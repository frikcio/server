from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import BoardModel, User, TopicModel, PostModel
from boards.views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        self.board = BoardModel.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.topic = TopicModel.objects.create(name='Hello, world', board=self.board, owner=user)
        PostModel.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        url = reverse('topic_posts', kwargs={'board_pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/board/{self.board.pk}/topic/{self.topic.pk}/')
        self.assertEquals(view.func.view_class, PostListView)
