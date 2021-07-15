from faker import Factory

from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.factories import UserFactory
from boards.factories import BoardFactory, TopicFactory, PostFactory
from boards.models import Board, Topic, Post
from boards.views import PostListView


fake = Factory.create()


class TopicPostsTests(TestCase):
    def setUp(self):
        board = BoardFactory()
        user = UserFactory()
        self.topic_1, topic_2 = TopicFactory.create_batch(2, board=board, owner=user)
        self.post_1 = PostFactory(topic=self.topic_1, created_by=user)
        self.post_2 = PostFactory(topic=topic_2, created_by=user)
        self.kwargs = {'board_pk': board.pk, 'topic_pk': self.topic_1.pk}
        self.url = reverse('topic_posts', kwargs=self.kwargs)
        self.client.force_login(user=user)

    def test_get_queryset(self):
        # Check that will get correctly queryset
        request = RequestFactory().get(self.url)
        view = PostListView()
        view.setup(request=request)
        view.kwargs.update(self.kwargs)
        queryset = view.get_queryset()
        self.assertIn(self.post_1, queryset)
        self.assertNotIn(self.post_2, queryset)

    def test_get_context_data(self):
        # Check that context contains new value
        response = self.client.get(self.url)
        self.assertIn("topic", response.context)

    def test_increase_topic_view(self):
        # Check that topic's views are increase, when render template
        self.client.get(self.url)
        topic = Topic.objects.first()
        self.assertNotEqual(topic.views, self.topic_1.views)

