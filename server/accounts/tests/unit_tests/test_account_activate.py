import os

from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve, reverse_lazy
from django.contrib.auth.tokens import default_token_generator

from boards.models import User
from accounts.views import AccountActivateView

import base64


class AccountActivateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_guy",
                                             email="test_guy@example.com",
                                             password="52654936abcdA",
                                             is_active=False)
        self.token = default_token_generator.make_token(self.user)
        uid64 = base64.urlsafe_b64encode(str(self.user.pk).encode()).decode()
        kwargs = {"uid64": uid64, "token": self.token}
        self.url = f"http://0.0.0.0:{os.environ['SERVER_PORT']}{reverse('activate_user', kwargs=kwargs)}"
        self.activate_url = f"http://0.0.0.0:{os.environ['SERVER_PORT']}/activate/{uid64}/activate_user/"
        request = RequestFactory().post(self.url)
        self.view = AccountActivateView()
        self.view.setup(request=request)
        self.view.kwargs.update(kwargs)

    def test_get_user_success(self):
        #   get user if get correctly uid64 or token
        url_user = self.view.get_user()
        db_user = User.objects.first()
        self.assertEquals(url_user, db_user)

    def test_get_user_fail(self):
        #   get None if get wrong uid64 or token
        self.view.kwargs['uid64'] = 'MktR=='
        url_user = self.view.get_user()
        self.assertIsNone(url_user)


    def test_get_context_data_if_link_is_not_valid(self):
        #   if link is not valid get "title" and "valid_link=False" at the template
        self.view.valid_link = False
        context = self.view.get_context_data()
        self.assertEqual(context["valid_link"], False)
        self.assertIn("title", context)

    def test_user_is_active(self):
        #   if transfer correct data, user is began active
        session = self.client.session
        session["_verification_token"] = self.token
        session.save()
        self.client.post(self.activate_url)
        user = User.objects.first()
        self.assertTrue(user.is_active)

    def test_user_is_not_active(self):
        #   if transfer wrong data, user is still not active
        session = self.client.session
        session["_verification_token"] = "Some-Wrong_token"
        session.save()
        self.client.post(self.activate_url)
        user = User.objects.first()
        self.assertFalse(user.is_active)

