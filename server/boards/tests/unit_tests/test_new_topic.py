from faker import Factory
import factory

from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory, GroupPermissions
from boards.factories import BoardFactory
from boards.models import Topic, Post


fake = Factory.create()

class TestNewTopic(TestCase):
    def setUp(self):
        self.board = BoardFactory()
        user = UserFactory()
        readers_group = get_object_or_404(Group, name='readers')
        writers_group = get_object_or_404(Group, name='writers')
        GroupPermissions.add_writers_permissions(writers_group)
        user.groups.add(writers_group)
        self.client.force_login(user=user)
        self.data = {'name': fake.word(), 'message': fake.text()}
        self.url = reverse("new_topic", kwargs={"board_pk": self.board.pk})

    def test_get_context_data(self):
        # Check that context will contains new value
        response = self.client.get(self.url)
        self.assertIn("board", response.context)

    def test_topic_is_created(self):
        # Check that topic is created
        response = self.client.post(self.url, data=self.data)
        topics = Topic.objects.all()
        self.assertEqual(topics.count(), 1)
        self.assertEqual(topics.first().board, self.board)
        self.assertEqual(topics.first().owner, response.wsgi_request.user)

    def test_post_is_created(self):
        # Check that post is created
        response = self.client.post(self.url, data=self.data)
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 1)
        self.assertEqual(posts.first().created_by, response.wsgi_request.user)
        self.assertEqual(posts.first().message, self.data['message'])



