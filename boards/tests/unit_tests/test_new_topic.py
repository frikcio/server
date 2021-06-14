from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import BoardModel, User, TopicModel, PostModel
from boards.site_forms import NewTopicForm
from boards.views import NewTopicView


class TestNewTopic(TestCase):
    def setUp(self):
        self.board = BoardModel.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.force_login(user=user)

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        board_topics_url = reverse('board_topics', kwargs={'board_pk': self.board.pk})
        response = self.client.get(new_topic_url)
        self.assertContains(response, f'href="{board_topics_url}"')

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        data = {
            'name': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(TopicModel.objects.exists())
        self.assertTrue(PostModel.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        data = {
            'name': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(TopicModel.objects.exists())
        self.assertFalse(PostModel.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'board_pk': self.board.pk})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

