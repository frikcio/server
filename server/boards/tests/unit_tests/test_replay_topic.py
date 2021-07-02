from django.test import TestCase, RequestFactory
from django.urls import reverse

from faker import Factory

from accounts.models import User
from boards.models import Board, Topic, Post
from boards.views import ReplyTopicView

fake = Factory.create()


class ReplyTopicTests(TestCase):
    def setUp(self):
        username = fake.name().split(" ")[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        user = User.objects.create(username=username, email=fake.email(), password=fake.password())
        board = Board.objects.create(name=fake.word(), description=fake.text())
        self.topic = Topic.objects.create(name=fake.word(), board=board, owner=user)
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
