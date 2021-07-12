from faker import Factory

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Settings

User = get_user_model()

fake = Factory.create()


class ChangeMailingStatusTests(TestCase):
    def setUp(self):
        username = fake.name().split(' ')[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        self.user = User.objects.create_user(username=username, password=fake.password())
        self.user_settings = Settings.objects.create(user=self.user)
        self.client.force_login(user=self.user)
        self.url = reverse('account_settings', kwargs={'user_pk': self.user.pk})

    def test_change_mailing_status(self):
        # Check that mailing status changed
        mailing_status_before = self.user_settings.periodic_mailing
        self.client.post(self.url + '?status=true', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        mailing_status_after = Settings.objects.get(user__pk=self.user.pk).periodic_mailing
        self.assertNotEqual(mailing_status_before, mailing_status_after)

    def test_response_status_code(self):
        # Check that status code
        response = self.client.post(self.url + '?status=true', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 202)
