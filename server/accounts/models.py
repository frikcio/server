from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from django.conf import settings


class User(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)

    @property
    def age(self):
        return int((timezone.now().date() - self.birth_date).year)


class Config(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='config')
    send_reminder_email = models.BooleanField(default=False, blank=True, null=True)
