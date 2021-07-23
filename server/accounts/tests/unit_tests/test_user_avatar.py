from faker import Factory

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory


fake = Factory.create()


class AvatarGenerationTests(TestCase):
    def setUp(self):
        self.user = UserFactory(first_name='', last_name='')
        self.file = open('boards/static/images/avatar.png', 'rb')

    def tearDown(self):
        if self.user.avatar:
            self.user.avatar.storage.delete(self.user.avatar.name)

    def test_generation_if_user_has_own_avatar(self):
        # Not generate avatar if user upload own avatar
        self.user.avatar.save('default_avatar.png', self.file)
        self.user.first_name = fake.word()
        self.user.last_name = fake.word()
        self.user.save()
        self.assertIsNotNone(self.user.avatar.name)
        self.assertNotIn(self.user.initials, self.user.avatar.name)

    def test_generation_with_normal_full_name(self):
        # Generate avatar if user has full_name
        self.user.first_name = fake.word()
        self.user.last_name = fake.word()
        self.user.save()
        self.assertIsNotNone(self.user.avatar.name)
        self.assertIn(self.user.initials, self.user.avatar.name)

    def test_generation_with_one_of_user_names(self):
        # Generate avatar if user has one of his names
        self.user.first_name = fake.word()
        self.user.save()
        self.assertIsNotNone(self.user.avatar.name)
        self.assertIn(self.user.initials, self.user.avatar.name)

    def test_generation_without_full_name(self):
        # Avatar is None if user hasn't full_name
        self.assertIsNone(self.user.avatar.name)

    def test_generation_if_user_changed_full_name_and_already_has_generated_avatar(self):
        # Generate avatar if user changed one of his names and already has generated avatar
        self.user.first_name = fake.word()
        self.user.last_name = fake.word()
        self.user.save()
        old_initials = self.user.initials
        self.user.first_name = fake.word()
        self.user.last_name = fake.word()
        self.user.save()
        new_initials = self.user.initials
        self.assertIsNotNone(self.user.avatar.name)
        self.assertNotEqual(old_initials, new_initials)
        self.assertNotIn(old_initials, self.user.avatar.name)
        self.assertIn(new_initials, self.user.avatar.name)

    def test_generation_if_user_swapped_names(self):
        # Generate avatar if user deleted first_name and wrote last_name
        self.user.first_name = fake.word()
        self.user.save()
        old_initials = self.user.initials
        self.user.first_name = ''
        self.user.last_name = fake.word()
        self.user.save()
        new_initials = self.user.initials
        self.assertIsNotNone(self.user.avatar.name)
        self.assertNotIn(old_initials, self.user.avatar.name)
        self.assertNotEqual(old_initials, new_initials)
        self.assertNotIn(f'{old_initials}{new_initials}', self.user.avatar.name)
        self.assertIn(new_initials, self.user.avatar.name)

    def test_generation_without_full_name_if_user_has_generated_avatar(self):
        # Delete generated avatar if user hasn't full_name
        self.user.first_name = fake.word()
        self.user.last_name = fake.word()
        self.user.save()
        old_initials = self.user.initials
        self.user.first_name = ''
        self.user.last_name = ''
        self.user.save()
        new_initials = self.user.initials
        self.assertNotEqual(old_initials, new_initials)
        self.assertIsNone(self.user.avatar.name)


class DeleteAvatarTests(TestCase):
    def setUp(self):
        self.user = UserFactory(first_name='', last_name='')
        file = open('boards/static/images/avatar.png', 'rb')
        self.old_file_name = 'default_avatar.png'
        self.user.avatar.save(self.old_file_name, file)
        self.client.force_login(user=self.user)
        self.url = reverse('delete_avatar', kwargs={'user_pk': self.user.pk})

    def tearDown(self):
        if self.user.avatar:
            self.user.avatar.storage.delete(self.user.avatar.name)

    def test_delete_avatar_if_user_has_full_name(self):
        # Delete old avatar and generate initial_avatar
        self.user.first_name = fake.word()
        self.user.last_name = fake.word()
        self.user.save()
        response = self.client.delete(self.url)
        new_file = get_user_model().objects.get(pk=self.user.pk).avatar
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(self.user.avatar.name)
        self.assertNotIn(self.old_file_name, new_file.name)
        self.assertIn(self.user.initials, new_file.name)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, 200)

    def test_delete_avatar_if_user_has_one_of_his_names(self):
        # Delete old avatar and generate initial_avatar if user has one of his names
        self.user.first_name = fake.word()
        self.user.save()
        response = self.client.delete(self.url)
        new_file = get_user_model().objects.get(pk=self.user.pk).avatar
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(self.user.avatar.name)
        self.assertNotIn(self.old_file_name, new_file.name)
        self.assertIn(self.user.initials, new_file.name)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, 200)

    def test_delete_avatar_if_user_without_full_name(self):
        # Delete avatar and not generate initial avatar without full_name
        response = self.client.delete(self.url)
        new_file = get_user_model().objects.get(pk=self.user.pk).avatar
        self.assertEquals(response.status_code, 200)
        self.assertEquals('', new_file.name)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, 204)