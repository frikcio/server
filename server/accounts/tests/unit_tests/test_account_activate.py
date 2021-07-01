from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve, reverse_lazy
from django.contrib.auth.tokens import default_token_generator

from boards.models import User
from accounts.views import AccountActivateView

import base64


class AccountActivateViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test_guy",
                                        email="test_guy@example.com",
                                        password="52654936abcdA",
                                        is_active=False)
        token = default_token_generator.make_token(user)
        uid64 = base64.urlsafe_b64encode(str(user.pk).encode()).decode()
        kwargs = {"uid64": uid64, "token": token}
        self.url = f'http:/{reverse("activate_user", kwargs=kwargs)}'
        request = RequestFactory().post(self.url)
        self.view = AccountActivateView()
        self.view.setup(request=request)
        self.view.kwargs.update(kwargs)

    def test_get_object_success(self):
        #   get user if get correctly uid64 or token
        url_user = self.view.get_user()
        db_user = User.objects.first()
        self.assertEquals(url_user, db_user)

    def test_get_object_fail(self):
        #   get None if get wrong uid64 or token
        self.view.kwargs['uid64'] = 'MktR=='
        url_user = self.view.get_user()
        self.assertIsNone(url_user)

    def test_get_context_data_if_link_is_valid(self):
        #   if link is valid, at template we get only "valid_link"
        self.view.valid_link = True
        context = self.view.get_context_data()
        self.assertIn("valid_link", context)
        self.assertEqual(context["valid_link"], True)
        self.assertNotIn("title", context)

    def test_get_context_data_if_link_is_not_valid(self):
        #   if link is not valid get "title" and "valid_link=False" at the template
        self.view.valid_link = False
        context = self.view.get_context_data()
        self.assertEqual(context["valid_link"], False)
        self.assertIn("title", context)

    def test_redirect(self):
        response = self.client.post(self.url)
        self.assertRedirects(response=response, expected_url=reverse_lazy("profile"))
