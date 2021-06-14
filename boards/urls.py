from django.urls import path

from boards.views import BoardListView, TopicListView, NewTopicView, PostListView, ReplyTopicView, PostUpdateView

board_url = 'board/<int:board_pk>/'
topic_url = 'topic/<int:topic_pk>/'
post_url = 'post/<int:post_pk>/'

urlpatterns = [
    path('', BoardListView.as_view(), name='home'),
    path(board_url, TopicListView.as_view(), name='board_topics'),
    path(board_url + 'new/', NewTopicView.as_view(), name='new_topic'),
    path(board_url + topic_url, PostListView.as_view(), name='topic_posts'),
    path(board_url + topic_url + 'reply/', ReplyTopicView.as_view(), name='reply_topic'),
    path(board_url + topic_url + post_url + 'edit/', PostUpdateView.as_view(), name='edit_post'),
]
