import factory

from accounts.factories import UserFactory
from .models import Board, Topic, Post


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    name = factory.Faker('name')
    description = factory.Faker('text')


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Faker('word')
    board = factory.SubFactory(BoardFactory)
    owner = factory.SubFactory(UserFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    message = factory.Faker('text')
    topic = factory.SubFactory(TopicFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
