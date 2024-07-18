import logging
from django.db import connection
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bookmarks.tasks import send_event_reminders

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def check_tables_and_start_scheduler(**kwargs):
    with connection.cursor() as cursor:
        cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE tablename = 'django_apscheduler_djangojob'")
        if cursor.fetchone():
            scheduler.add_jobstore(DjangoJobStore(), "default")

            # Добавьте вашу задачу в планировщик
            scheduler.add_job(
                send_event_reminders,
                trigger=IntervalTrigger(minutes=1),  # Укажите интервал времени
                id='send_event_reminders',  # Уникальный ID для задачи
                replace_existing=True
            )

            scheduler.start()
            logger.info("Scheduler started successfully and tasks have been added.")
        else:
            logger.warning("Scheduler tables do not exist yet. Scheduler not started.")
