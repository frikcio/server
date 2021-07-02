from django.test import TestCase, RequestFactory
from django.urls import reverse
from faker import Factory

from accounts.models import User
from boards.models import Board, Topic, Post
from boards.views import NewTopicView

fake = Factory.create()


class TestNewTopic(TestCase):
    def setUp(self):
        username = fake.name().split(" ")[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        self.board = Board.objects.create(name=fake.word(), description=fake.text())
        user = User.objects.create_user(username=username, email=fake.email(), password=fake.password())
        self.client.force_login(user=user)
        self.data = {"name": fake.word(), "message": fake.text()}
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



