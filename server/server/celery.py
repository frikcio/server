import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_reminder_email': {
        'task': 'accounts.tasks.email_distribution',
        'schedule': crontab(hour=14, minute=0, day_of_week='1,2,3,4,5')

    }
}
app.conf.timezone = 'Europe/Kiev'
