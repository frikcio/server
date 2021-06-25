from celery import shared_task

@shared_task
def send_email(user)
	user.email_user(subject=user, message="hi", from="develop Team")