from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from .choices import Gender


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.NOT_SELECTED)
    avatar = models.ImageField(blank=True, null=True, upload_to=f'accounts/')

    def __str__(self):
        return self.username

    def get_upload_path(self):
        return f'accounts/{self.username}/avatar/'


class Settings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    periodic_mailing = models.BooleanField(default=False)
