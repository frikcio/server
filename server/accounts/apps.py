from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from .signals import generate_avatar


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_save.connect(generate_avatar, sender=get_user_model())
