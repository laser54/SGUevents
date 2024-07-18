from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from bookmarks.tasks import send_event_reminders

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", minutes=1, id="scheduler.periodic_task", replace_existing=True)
def periodic_task():
    send_event_reminders()

register_events(scheduler)

def start():
    scheduler.start()
