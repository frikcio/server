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
def email_distribution():
    # send emails only for willing users
    recipients = User.objects.filter(settings__periodic_mailing=True)
    emails = []
    for user in recipients:
        message = f'Hi {user}\n you get this email because you accept periodic mailing'
        email_data = (user, message, "develop@team.com", [user.email])
        emails.append(email_data)
    send_mass_mail(emails, fail_silently=True)
