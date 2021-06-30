from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve

from server.celery import app
from boards.models import User
from accounts.views import RegisterView, send_verification_email


class RegistrationTest(TestCase):
    def setUp(self):
        self.data = {'username': 'test_guy',
                     'email': 'test_guy@example.com',
                     'password1': '52654936abcdA',
                     'password2': '52654936abcdA',
                     }
        self.url = reverse('register')

    def test_user_is_created(self):
        self.client.post(self.url, self.data)
        queryset = User.objects.all()
        self.assertEquals(queryset.count(), 1)

    def test_user_is_not_active(self):
        self.client.post(self.url, self.data)
        user = User.objects.first()
        self.assertFalse(user.is_active)
