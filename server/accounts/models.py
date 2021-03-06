from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from .choices import Gender


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.NOT_SELECTED)
    avatar = models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d/%H:%M:%S')

    def __str__(self):
        return self.username

    @property
    def initials(self):
        initials = ''
        full_name = self.get_full_name()
        text = full_name.strip()
        if text:
            split_text = text.split(' ')
            if len(split_text) > 1:
                initials = split_text[0][0] + split_text[-1][0]
            else:
                initials = split_text[0][0]

        return initials.upper()


class Settings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    periodic_mailing = models.BooleanField(default=False)
