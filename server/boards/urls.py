from django.urls import path

from .views import *

urlpatterns = [
    path('', BoardListView.as_view(), name='home'),
    path('board/new/', NewBoardView.as_view(), name='new_board'),
    path('board/<int:board_pk>/', TopicListView.as_view(), name='board_topics'),
    path('board/<int:board_pk>/new/', NewTopicView.as_view(), name='new_topic'),
    path('board/<int:board_pk>/topic/<int:topic_pk>/', PostListView.as_view(), name='topic_posts'),
    path('board/<int:board_pk>/topic/<int:topic_pk>/reply/', ReplyTopicView.as_view(), name='reply_topic'),
    path('board/<int:board_pk>/topic/<int:topic_pk>/post/<int:post_pk>/edit/', PostUpdateView.as_view(),
         name='edit_post'),
]
