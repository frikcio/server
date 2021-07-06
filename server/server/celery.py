import os

from celery import Celery
from celery.schedules import crontab

from accounts.tasks import reminder

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'reminder': {
        'task': 'accounts.tasks.reminder',
        'schedule': crontab(hour=14, day_of_week='1,2,3,4,5')

    }
}
