from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGUevents.settings')

app = Celery('SGUevents')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
