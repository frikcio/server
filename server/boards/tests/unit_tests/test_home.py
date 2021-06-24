from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import BoardModel
from boards.views import BoardListView, TopicListView


class TestHome(TestCase):
    def setUp(self):
        self.board = BoardModel.objects.create(name='Django', description='django description')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_to_topics_page(self):
        topics_url = reverse('board_topics', kwargs={'board_pk': self.board.pk})
        self.assertContains(self.response, f"{topics_url}")


class TestBoardTopics(TestCase):
    def setUp(self):
        self.board = BoardModel.objects.create(name='Django', description='django description')
        self.board_topics_url = reverse('board_topics', kwargs={'board_pk': self.board.pk})
        self.home_url = reverse('home')

    def test_board_topics_status_code(self):
        response = self.client.get(self.board_topics_url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_not_found(self):
        incorrect_url = reverse('board_topics', kwargs={'board_pk': 999})
        response = self.client.get(incorrect_url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/board/1/')
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_to_home_page(self):
        response = self.client.get(self.board_topics_url)
        self.assertContains(response, f'{self.home_url}')

    def test_board_topics_navigator_links(self):
        new_topic_url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        response = self.client.get(self.board_topics_url)
        self.assertContains(response, f'{self.home_url}')
        self.assertContains(response, f'{new_topic_url}')
