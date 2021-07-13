from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


class NewBoardView(PermissionRequiredMixin, CreateView):
    permission_required = 'boards.add_board'
    model = Board
    template_name = 'board/new_board.html'
    fields = ('name', 'description')
    login_url = '/login/'
    success_url = reverse_lazy('home')


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board/home.html'
    paginate_by = 5


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'board/board_topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # Append new value to board_topics template
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        # Get topics only for certain board, order by last update and append posts count for every topic
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_pk'))
        queryset = self.board.topics.order_by('-last_update').annotate(replies=Count('posts'))
        return queryset


class NewTopicView(PermissionRequiredMixin, CreateView):
    permission_required = 'boards.add_topic'
    form_class = NewTopicForm
    template_name = 'board/new_topic.html'
    pk_url_kwarg = 'board_pk'
    login_url = '/login/'

    def form_valid(self, form):
        # Create new topic and first post for this topic
        topic = form.save(commit=False)
        topic.board = Board.objects.get(pk=self.kwargs['board_pk'])
        topic.owner = self.request.user
        topic.save()
        Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=self.request.user
        )
        return redirect('topic_posts', board_pk=topic.board.pk, topic_pk=topic.pk)

    def get_context_data(self, **kwargs):
        # Append new value to new_topic template
        kwargs['board'] = Board.objects.get(pk=self.kwargs['board_pk'])
        return super().get_context_data(**kwargs)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'board/topic_posts.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        # Update topic's view, when template rendering and append new value to topic_posts template
        session_key = f'viewed_topic_{self.topic.pk}'
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        # Get posts only for curtain topic and oder by created at
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


class ReplyTopicView(PermissionRequiredMixin, CreateView):
    permission_required = 'boards.add_post'
    form_class = PostForm
    template_name = 'board/reply_topic.html'
    pk_url_kwarg = 'board_pk'
    login_url = '/login/'

    def form_valid(self, form):
        # Create new post update topic's last update and redirect to current posts page
        post = form.save(commit=False)
        topic = Topic.objects.get(pk=self.kwargs['topic_pk'])
        post.topic = topic
        post.created_by = self.request.user
        with transaction.atomic():
            post.save()
            topic.save()
        topic_url = reverse('topic_posts', kwargs={'board_pk': topic.board.pk, 'topic_pk': topic.pk})
        topic_post_url = f'{topic_url}?page={topic.get_page_count()}#{post.pk}'
        return redirect(topic_post_url)

    def get_context_data(self, **kwargs):
        # Append new value to reply_topic template
        kwargs['topic'] = Topic.objects.get(pk=self.kwargs['topic_pk'])
        return super().get_context_data(**kwargs)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'boards.update_post'
    login_url = '/login/'
    model = Post
    fields = ('message',)
    template_name = 'board/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        # Get current user's posts
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        # Update post's updated by
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)
