from django.test import TestCase
from django.urls import reverse

from boards.models import BoardModel, User, TopicModel, PostModel


class ReplyTopicTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.board = BoardModel.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.client.force_login(user=user)
        self.topic = TopicModel.objects.create(name='Hello, world', board=self.board, owner=user)
        PostModel.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'board_pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    pass


class ReplyTopicTests(ReplyTopicTestCase):
    pass


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        response = self.client.post(self.url, data={'message': 'test-message'})
        url = reverse('topic_posts', kwargs={'board_pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(response, topic_posts_url)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    pass
