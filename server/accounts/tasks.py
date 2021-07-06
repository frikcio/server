import base64

from celery import shared_task

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


@shared_task
def send_verification_email(user_pk, absolute_url):
    user = get_user_model().objects.get(pk=user_pk)
    token = default_token_generator.make_token(user)
    uid64 = base64.urlsafe_b64encode(str(user.pk).encode()).decode()
    message = f'Hi {user}\n you just register in our site\n To continue registration please follow: \n' \
              f'{absolute_url}activate/{uid64}/{token}/' \
              f' to activate your account'
    user.email_user(subject=user, message=message, from_email="develop Team")


@shared_task
def reminder(user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    message = f'Hi {user}\n your lunch will be in 5 minutes'
    user.email_user(subject=user, message=message, from_email="develop Team")
