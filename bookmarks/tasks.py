# bookmarks/tasks.py

import datetime
from django.utils import timezone
from django.db.models import Q
from bookmarks.models import Registered
from users.telegram_utils import send_message_to_user
import logging

logger = logging.getLogger(__name__)

def send_event_reminders():
    logger.info("Starting send_event_reminders task.")
    now = timezone.now()
    one_day_later_start = now + datetime.timedelta(days=1)
    one_day_later_end = now + datetime.timedelta(days=1, minutes=5)
    one_hour_later_start = now + datetime.timedelta(hours=1)
    one_hour_later_end = now + datetime.timedelta(hours=1, minutes=5)
    five_minutes_later_start = now + datetime.timedelta(minutes=5)
    five_minutes_later_end = now + datetime.timedelta(minutes=10)

    logger.info(f"Checking for events starting between {one_day_later_start} and {one_day_later_end}")
    logger.info(f"Checking for events starting between {one_hour_later_start} and {one_hour_later_end}")
    logger.info(f"Checking for events starting between {five_minutes_later_start} and {five_minutes_later_end}")

    events = Registered.objects.filter(
        Q(start_datetime__range=(one_day_later_start, one_day_later_end)) |
        Q(start_datetime__range=(one_hour_later_start, one_hour_later_end)) |
        Q(start_datetime__range=(five_minutes_later_start, five_minutes_later_end))
    ).select_related('user', 'online', 'offline', 'attractions', 'for_visiting')

    logger.info(f"Found {events.count()} events to send reminders for.")

    for event in events:
        if event.online:
            event_obj = event.online
        elif event.offline:
            event_obj = event.offline
        elif event.attractions:
            event_obj = event.attractions
        elif event.for_visiting:
            event_obj = event.for_visiting

        message = f"Напоминание: мероприятие '{event_obj.name}' начинается скоро."
        send_message_to_user(event.user.telegram_id, message)
        logger.info(f"Sent reminder to {event.user.username} for event {event_obj.name}.")
