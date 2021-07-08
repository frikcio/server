from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)

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
