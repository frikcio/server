from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from boards.models import Post, Board, Topic, User
from boards.views import PostUpdateView


class TestsPostUpdateView(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='testguy1', email='testguy1@example.com', password='test')
        user2 = User.objects.create_user(username='testguy2', email='testguy2@example.com', password='test')
        board = Board.objects.create(name='Board', description='description')
        topic = Topic.objects.create(name='Topic', board=board, owner=user1)
        self.post1 = Post.objects.create(message='first testguy1', topic=topic, created_by=user1, updated_by=user1)
        self.post2 = Post.objects.create(message='first testguy2', topic=topic, created_by=user2, updated_by=user2)
        self.url = reverse('edit_post', kwargs={"board_pk": board.pk, "topic_pk": topic.pk, "post_pk": self.post1.pk})
        request = RequestFactory().post(self.url, data={"message": "second"})
        request.user = user1
        self.view = PostUpdateView()
        self.view.setup(request=request)

    def test_get_filter_queryset(self):
        queryset = self.view.get_queryset()
        self.assertIn(self.post1, queryset)
        self.assertNotIn(self.post2, queryset)

