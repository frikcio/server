import base64

from celery import shared_task

from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


@shared_task
def send_verification_email(user_pk, absolute_url):
    # send verification email for user
    user = User.objects.get(pk=user_pk)
    token = default_token_generator.make_token(user)
    uid64 = base64.urlsafe_b64encode(str(user.pk).encode()).decode()
    message = f'Hi {user}\n you just register in our site\n To continue registration please follow: \n' \
              f'{absolute_url}activate/{uid64}/{token}/' \
              f' to activate your account'
    user.email_user(subject=user, message=message, from_email="develop Team")


@shared_task
def mailing():
    # send reminder email only for users with config.send_reminder_email = True
    messages = []
    for user in User.objects.filter(settings__periodic_mailing=True):
        message = f'Hi {user}\n your lunch will be in 5 minutes'
        msg = (user, message, "develop@team.com", [user.email])
        messages.append(msg)
    send_mass_mail(messages, fail_silently=False)
