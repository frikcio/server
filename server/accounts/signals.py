from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import RemindAccess


@receiver(post_save, sender=get_user_model())
def profile_create(sender, instance, created, **kwargs):
    if created:
        RemindAccess.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def profile_update(sender, instance, **kwargs):
    instance.profile.save()
