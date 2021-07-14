from django.contrib.auth.models import Group
from faker import Factory

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


fake = Factory.create()


User = get_user_model()


class RegistrationTest(TestCase):
    def setUp(self):
        username = fake.name().split(" ")[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        password = fake.password()
        self.group = Group.objects.first()
        self.data = {'username': username,
                     'email': fake.email(),
                     'password1': password,
                     'password2': password,
                     'groups': self.group.pk,
                     }
        self.url = reverse('register')

    def test_user_is_created(self):
        # Check that user is created
        self.client.post(self.url, self.data)
        queryset = User.objects.all()
        self.assertEquals(queryset.count(), 1)

    def test_user_is_not_active(self):
        # Check that user is created and not active
        self.client.post(self.url, self.data)
        user = User.objects.first()
        self.assertFalse(user.is_active)

    def test_user_group(self):
        # Check that user is contains in group
        self.client.post(self.url, self.data)
        another_group = Group.objects.last()
        user = User.objects.first()
        self.assertIn(self.group, user.groups.all())
        self.assertNotIn(another_group, user.groups.all())
