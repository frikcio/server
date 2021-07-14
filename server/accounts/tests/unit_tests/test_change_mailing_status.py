from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from accounts.models import Settings


class ChangeMailingStatusTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_settings = Settings.objects.create(user=self.user)
        self.client.force_login(user=self.user)
        self.url = reverse('account_settings', kwargs={'user_pk': self.user.pk})

    def test_change_mailing_status(self):
        # Check that mailing status changed
        mailing_status_before = self.user_settings.periodic_mailing
        response = self.client.post(self.url + '?status=true', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        mailing_status_after = Settings.objects.get(user__pk=self.user.pk).periodic_mailing
        self.assertNotEqual(mailing_status_before, mailing_status_after)
        self.assertEqual(response.status_code, 202)

    def test_url_not_have_params(self):
        # Check that if url not have query params, return status_code 400
        mailing_status_before = self.user_settings.periodic_mailing
        response = self.client.post(self.url, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        mailing_status_after = Settings.objects.get(user__pk=self.user.pk).periodic_mailing
        self.assertEqual(mailing_status_before, mailing_status_after)
        self.assertEqual(response.status_code, 400)
