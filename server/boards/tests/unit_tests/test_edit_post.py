from faker import Factory

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from boards.models import Post, Board, Topic
from boards.views import PostUpdateView

User = get_user_model()

fake = Factory.create()


class TestsPostUpdateView(TestCase):
    def setUp(self):
        username1 = fake.name().split(" ")[0]  # fake.name() return "Name Surname", so I split the string and get "Name"
        username2 = fake.name().split(" ")[0]
        self.user1 = User.objects.create_user(username=username1, email=fake.email(), password=fake.password())
        self.user2 = User.objects.create_user(username=username2, email=fake.email(), password=fake.password())
        board = Board.objects.create(name=fake.word(), description=fake.text())
        topic = Topic.objects.create(name=fake.word(), board=board, owner=self.user1)
        self.post1 = Post.objects.create(message=fake.text(), topic=topic, created_by=self.user1, updated_by=self.user1)
        self.post2 = Post.objects.create(message=fake.text(), topic=topic, created_by=self.user2, updated_by=self.user2)
        self.url = reverse('edit_post', kwargs={"board_pk": board.pk, "topic_pk": topic.pk, "post_pk": self.post1.pk})
        request = RequestFactory().post(self.url, data={"message": fake.text()})
        request.user = self.user1
        self.view = PostUpdateView()
        self.view.setup(request=request)

    def test_get_filter_queryset(self):
        #   get queryset with post with post1 and without post2
        queryset = self.view.get_queryset()
        self.assertIn(self.post1, queryset)
        self.assertNotIn(self.post2, queryset)

    def test_post_updated_by_owner(self):
        #   if request sends by post's user, update post's  message, updated_at and updated_by
        self.client.force_login(user=self.user1)
        self.client.post(self.url, data={"message": fake.text()})
        not_updated_post = self.post1
        updated_post = Post.objects.get(pk=self.post1.pk)
        self.assertEqual(not_updated_post.updated_by, updated_post.updated_by)
        self.assertNotEqual(not_updated_post.updated_at, updated_post.updated_at)
        self.assertNotEqual(not_updated_post.message, updated_post.message)

    def test_post_updated_by_not_owner(self):
        #    if request sends not by post's user, update nothing
        self.client.force_login(user=self.user2)
        self.client.post(self.url, data={"message": fake.text()})
        not_updated_post = self.post1
        updated_post = Post.objects.get(pk=self.post1.pk)
        self.assertEqual(not_updated_post.updated_by, updated_post.updated_by)
        self.assertEqual(not_updated_post.updated_at, updated_post.updated_at)
        self.assertEqual(not_updated_post.message, updated_post.message)
