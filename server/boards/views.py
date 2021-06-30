from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


class NewBoardView(LoginRequiredMixin, CreateView):
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
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_pk'))
        queryset = self.board.topics.order_by('-last_update').annotate(replies=Count('posts'))
        return queryset


class NewTopicView(LoginRequiredMixin, CreateView):
    form_class = NewTopicForm
    template_name = 'board/new_topic.html'
    pk_url_kwarg = 'board_pk'
    login_url = '/login/'

    def form_valid(self, form):
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
        kwargs['board'] = Board.objects.get(pk=self.kwargs['board_pk'])
        return super().get_context_data(**kwargs)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'board/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_pk'),
                                       pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


class ReplyTopicView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'board/reply_topic.html'
    pk_url_kwarg = 'board_pk'
    login_url = '/login/'

    def form_valid(self, form):
        post = form.save(commit=False)
        topic = Topic.objects.get(pk=self.kwargs['topic_pk'])
        post.topic = topic
        post.created_by = self.request.user
        with transaction.atomic():
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
        topic_url = reverse('topic_posts', kwargs={'board_pk': topic.board.pk, 'topic_pk': topic.pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.pk,
            page=topic.get_page_count()
        )
        return redirect(topic_post_url)

    def get_context_data(self, **kwargs):
        kwargs['topic'] = Topic.objects.get(pk=self.kwargs['topic_pk'])
        return super().get_context_data(**kwargs)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Post
    fields = ('message',)
    template_name = 'board/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)
