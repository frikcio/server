from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
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
        request = RequestFactory().post(reverse("account_activate", kwargs={"uid64": uid64,
                                                                            "token": token}))
        self.view = AccountActivateView()
        self.view.setup(request)

    def test_get_object(self):
        url_user = self.view.get_object()
        db_user = User.objects.first()
        self.assertIs(url_user, db_user)

    def test_get_context_data(self):
        context = self.view.get_context_data()
        self.assertIn("valid_link", context)
