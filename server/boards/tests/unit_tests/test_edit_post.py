from faker import Factory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.choices import GroupChoices
from accounts.factories import UserFactory, add_readers_permissions_to
from boards.factories import BoardFactory, TopicFactory, PostFactory
from boards.models import Post, Board, Topic
from boards.views import PostUpdateView


User = get_user_model()

fake = Factory.create()


class TestsPostUpdateView(TestCase):
    def setUp(self):
        self.user_1, self.user_2 = UserFactory.create_batch(2)
        readers_group = Group.objects.get(name=GroupChoices.READERS)
        add_readers_permissions_to(readers_group)
        self.user_1.groups.add(readers_group)
        self.user_2.groups.add(readers_group)
        board = BoardFactory()
        topic = TopicFactory(board=board, owner=self.user_1)
        self.post_1 = PostFactory(topic=topic, created_by=self.user_1, updated_by=self.user_1)
        self.post_2 = PostFactory(topic=topic, created_by=self.user_2, updated_by=self.user_2)
        self.url = reverse('edit_post', kwargs={'board_pk': board.pk, 'topic_pk': topic.pk, 'post_pk': self.post_1.pk})

    def test_get_filter_queryset(self):
        # Get queryset with post with post_1 and without post_2
        request = RequestFactory().post(self.url, data={'message': fake.text()})
        request.user = self.user_1
        view = PostUpdateView()
        view.setup(request=request)
        queryset = view.get_queryset()
        self.assertIn(self.post_1, queryset)
        self.assertNotIn(self.post_2, queryset)

    def test_post_updated_by_owner(self):
        # Update message, updated_at and updated_by if request sends by post's owner
        self.client.force_login(user=self.user_1)
        response = self.client.post(self.url, data={'message': fake.text()})
        not_updated_post = self.post_1
        updated_post = Post.objects.get(pk=self.post_1.pk)
        self.assertEqual(not_updated_post.updated_by, updated_post.updated_by)
        self.assertNotEqual(not_updated_post.updated_at, updated_post.updated_at)
        self.assertNotEqual(not_updated_post.message, updated_post.message)

    def test_post_updated_by_not_owner(self):
        # Update nothing if request sends by not post's owner
        self.client.force_login(user=self.user_2)
        self.client.post(self.url, data={'message': fake.text()})
        not_updated_post = self.post_1
        updated_post = Post.objects.get(pk=self.post_1.pk)
        self.assertEqual(not_updated_post.updated_by, updated_post.updated_by)
        self.assertEqual(not_updated_post.updated_at, updated_post.updated_at)
        self.assertEqual(not_updated_post.message, updated_post.message)
