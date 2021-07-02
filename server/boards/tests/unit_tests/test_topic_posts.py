from faker import Factory

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse


from boards.models import Board, Topic, Post
from boards.views import PostListView

User = get_user_model()

fake = Factory.create()


class TopicPostsTests(TestCase):
    def setUp(self):
        username = fake.name().split(" ")[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        board1 = Board.objects.create(name=fake.word(), description=fake.text())
        board2 = Board.objects.create(name=fake.word(), description=fake.text())
        user = User.objects.create_user(username=username, email=fake.email(), password=fake.password())
        self.topic1 = Topic.objects.create(name=fake.word(), board=board1, owner=user)
        topic2 = Topic.objects.create(name=fake.word(), board=board2, owner=user)
        self.post1 = Post.objects.create(message=fake.text(), topic=self.topic1, created_by=user)
        self.post2 = Post.objects.create(message=fake.text(), topic=topic2, created_by=user)
        kwargs = {'board_pk': board1.pk, 'topic_pk': self.topic1.pk}
        self.url = reverse('topic_posts', kwargs=kwargs)
        request = RequestFactory().get(self.url)
        self.client.force_login(user=user)
        self.view = PostListView()
        self.view.setup(request=request)
        self.view.kwargs.update(kwargs)

    def test_get_queryset(self):
        # Check that will get correctly queryset
        queryset = self.view.get_queryset()
        self.assertIn(self.post1, queryset)
        self.assertNotIn(self.post2, queryset)

    def test_get_context_data(self):
        # Check that context contains new value
        response = self.client.get(self.url)
        self.assertIn("topic", response.context)

    def test_increase_topic_view(self):
        # Check that topic's views are increase, when render template
        self.client.get(self.url)
        topic = Topic.objects.first()
        self.assertNotEqual(topic.views, self.topic1.views)

