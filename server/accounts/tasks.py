import base64

from celery import shared_task
from django.conf import settings

from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

User = get_user_model()


@shared_task
def send_verification_email(user_pk, http_host):
    # send verification email for user
    user = User.objects.get(pk=user_pk)
    token = default_token_generator.make_token(user)
    uid64 = base64.urlsafe_b64encode(str(user.pk).encode()).decode()
    message = render_to_string('accounts/verification_email.html',
                               {'user': user.username, 'uid64': uid64, 'token': token, 'http_host': http_host})
    user.email_user(subject=user, message=message, from_email=settings.EMAIL_SENDER)


@shared_task
def distribute_emails():
    # send emails only for willing users
    recipients = User.objects.filter(settings__periodic_mailing=True)
    emails = []
    for user in recipients:
        message = render_to_string('accounts/distribution_email.html', {'user': user })
        email_data = (user, message, settings.EMAIL_SENDER, [user.email])
        emails.append(email_data)
    send_mass_mail(emails, fail_silently=True)
