import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    password = factory.Faker('password')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class GroupPermissions(object):
    @staticmethod
    def add_readers_permissions(group_name):
        post_list = Permission.objects.filter(codename__contains='post').exclude(codename__contains='delete')
        read_board = Permission.objects.get(codename='view_board')
        read_topic = Permission.objects.get(codename='view_topic')
        group_name.permissions.set(post_list)
        group_name.permissions.add(read_board, read_topic)

    @staticmethod
    def add_writers_permissions(group_name):
        board_list = Permission.objects.filter(codename__contains='board')
        topic_list = Permission.objects.filter(codename__contains='topic').exclude(codename__contains='delete')
        read_post = Permission.objects.get(codename='view_post')
        writers_permissions = board_list | topic_list
        group_name.permissions.set(writers_permissions)
        group_name.permissions.add(read_post)
