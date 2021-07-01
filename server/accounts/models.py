from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    confirm_email = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)

    @property
    def age(self):
        return int((timezone.now().date() - self.birth_date).year)
