from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGUevents.settings')

app = Celery('SGUevents')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.conf.beat_schedule = {
    'schedule-notifications-every-5-minutes': {
        'task': 'bookmarks.tasks.schedule_notifications',
        'schedule': crontab(minute='*/5'),  # каждые 5 минут
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
