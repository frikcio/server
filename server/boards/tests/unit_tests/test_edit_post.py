from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from faker import Factory

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.factories import UserFactory, GroupPermissions
from boards.factories import BoardFactory, TopicFactory, PostFactory
from boards.models import Post, Board, Topic
from boards.views import PostUpdateView


User = get_user_model()

fake = Factory.create()


class TestsPostUpdateView(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        readers_group = get_object_or_404(Group, name='readers')
        writers_group = get_object_or_404(Group, name='writers')
        GroupPermissions.add_writers_permissions(writers_group)
        GroupPermissions.add_readers_permissions(readers_group)
        self.user1.groups.add(readers_group)
        self.user2.groups.add(writers_group)
        board = BoardFactory()
        topic = TopicFactory(board=board, owner=self.user1)
        self.post1 = PostFactory(topic=topic, created_by=self.user1, updated_by=self.user1)
        self.post2 = PostFactory(topic=topic, created_by=self.user2, updated_by=self.user2)
        self.url = reverse('edit_post', kwargs={'board_pk': board.pk, 'topic_pk': topic.pk, 'post_pk': self.post1.pk})
        request = RequestFactory().post(self.url, data={'message': fake.text()})
        request.user = self.user1
        self.view = PostUpdateView()
        self.view.setup(request=request)

    def test_get_filter_queryset(self):
        # Get queryset with post with post1 and without post2
        queryset = self.view.get_queryset()
        self.assertIn(self.post1, queryset)
        self.assertNotIn(self.post2, queryset)

    def test_post_updated_by_owner(self):
        # Update message, updated_at and updated_by if request sends by post's owner
        self.client.force_login(user=self.user1)
        response = self.client.post(self.url, data={'message': fake.text()})
        not_updated_post = self.post1
        updated_post = Post.objects.get(pk=self.post1.pk)
        self.assertEqual(not_updated_post.updated_by, updated_post.updated_by)
        self.assertNotEqual(not_updated_post.updated_at, updated_post.updated_at)
        self.assertNotEqual(not_updated_post.message, updated_post.message)

    def test_post_updated_by_not_owner(self):
        # Update nothing if request sends by not post's owner
        self.client.force_login(user=self.user2)
        self.client.post(self.url, data={'message': fake.text()})
        not_updated_post = self.post1
        updated_post = Post.objects.get(pk=self.post1.pk)
        self.assertEqual(not_updated_post.updated_by, updated_post.updated_by)
        self.assertEqual(not_updated_post.updated_at, updated_post.updated_at)
        self.assertEqual(not_updated_post.message, updated_post.message)
