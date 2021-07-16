import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from boards.models import Post, Topic, Board
from django.db.models import Q

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    password = factory.Faker('password')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


def add_readers_permissions_to_group(group_name):
    board_lookup = Q(content_type__model=Post._meta.model_name)
    topic_lookup = Q(content_type__model=Topic._meta.model_name)
    post_permissions = Permission.objects.filter(content_type__model=Post._meta.model_name).exclude(
        codename__contains='delete')
    view_permissions = Permission.objects.filter(board_lookup | topic_lookup).filter(
        codename__contains='view')
    readers_permissions = post_permissions | view_permissions
    group_name.permissions.set(readers_permissions)


def add_writers_permissions_to_group(group_name):
    board_permissions = Permission.objects.filter(content_type__model=Board._meta.model_name)
    topic_permissions = Permission.objects.filter(content_type__model=Topic._meta.model_name).exclude(
        codename__contains='delete')
    view_post_permission = Permission.objects.filter(content_type__model=Post._meta.model_name).filter(
        codename__contains='view')
    writers_permissions = board_permissions | topic_permissions | view_post_permission
    group_name.permissions.set(writers_permissions)
