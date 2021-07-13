from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone


class GroupCreation(object):
    NAMES = ['readers', 'writers']

    def create(self):
        # Create users groups for server
        Group.objects.bulk_create([Group(name=name) for name in self.NAMES])  # Create all groups from GROUP_NAMES


class User(AbstractUser):
    class Gender(models.IntegerChoices):
        NOT_SELECTED = 0
        MAN = 1
        WOMAN = 2

    email = models.EmailField(unique=True, blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.NOT_SELECTED)

    def __str__(self):
        return self.username

    @property
    def age(self):
        return int((timezone.now().date() - self.birth_date).year)


class Settings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    periodic_mailing = models.BooleanField(default=False)

    def __str__(self):
        return ".periodic_mailing"
