from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGUevents.settings')

app = Celery('SGUevents')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    beat_schedule={
        'schedule_notifications_day': {
            'task': 'bookmarks.tasks.schedule_notifications',
            'schedule': crontab(hour='*', minute=0),  # Запускать каждый час
        },
        'schedule_notifications_hour': {
            'task': 'bookmarks.tasks.schedule_notifications',
            'schedule': crontab(minute='*/10'),  # Запускать каждые 10 минут
        },
        'schedule_notifications_minutes': {
            'task': 'bookmarks.tasks.schedule_notifications',
            'schedule': crontab(minute='*/1'),  # Запускать каждую минуту
        },
    },
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
