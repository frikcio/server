import base64
import os

from faker import Factory

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.views import AccountActivateView


fake = Factory.create()

User = get_user_model()


class AccountActivateViewTests(TestCase):
    def setUp(self):
        username = fake.name().split(" ")[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        self.user = User.objects.create_user(username=username,
                                             email=fake.email(),
                                             password=fake.password(),
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
        # Get user if get correctly uid64 or token
        url_user = self.view.get_user()
        db_user = User.objects.first()
        self.assertEquals(url_user, db_user)

    def test_get_user_fail(self):
        # Get None if get wrong uid64 or token
        self.view.kwargs['uid64'] = 'MktR=='
        url_user = self.view.get_user()
        self.assertIsNone(url_user)

    def test_get_context_data_if_link_is_not_valid(self):
        # Get values at the template if link is not valid 
        self.view.valid_link = False
        context = self.view.get_context_data()
        self.assertEqual(context["valid_link"], False)
        self.assertIn("title", context)

    def test_user_is_active(self):
        # Activate user if he sent correct data, 
        session = self.client.session
        session["_verification_token"] = self.token
        session.save()
        self.client.post(self.activate_url)
        user = User.objects.first()
        self.assertTrue(user.is_active)

    def test_user_is_not_active(self):
        # Not activete user if sent wrong data 
        session = self.client.session
        session["_verification_token"] = "Some-Wrong_token"
        session.save()
        self.client.post(self.activate_url)
        user = User.objects.first()
        self.assertFalse(user.is_active)

