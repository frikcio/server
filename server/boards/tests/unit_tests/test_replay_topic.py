from faker import Factory

from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory, GroupPermissions
from boards.factories import BoardFactory, TopicFactory
from boards.models import Board, Topic, Post

fake = Factory.create()


class ReplyTopicTests(TestCase):
    def setUp(self):
        user = UserFactory()
        board = BoardFactory()
        readers_group = get_object_or_404(Group, name='readers')
        writers_group = get_object_or_404(Group, name='writers')
        GroupPermissions.add_writers_permissions(writers_group)
        GroupPermissions.add_readers_permissions(readers_group)
        user.groups.add(readers_group)
        self.topic = TopicFactory(board=board, owner=user)
        self.client.force_login(user=user)
        self.url = reverse("reply_topic", kwargs={"board_pk": board.pk, "topic_pk": self.topic.pk})

    def test_get_context(self):
        # Check that context will contains new value
        response = self.client.get(self.url)
        self.assertIn("topic", response.context)

    def test_post_is_created(self):
        # Check that post will create
        response = self.client.post(self.url, data={"message": fake.text()})
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 1)
        self.assertEqual(posts.first().topic, self.topic)
        self.assertEqual(posts.first().created_by, response.wsgi_request.user)

    def test_topic_is_updated(self):
        # Check that topic will update when post will create
        self.client.post(self.url, data={"message": fake.text()})
        updated_topic = Topic.objects.first()
        self.assertNotEqual(updated_topic.last_update, self.topic.last_update)
