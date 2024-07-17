import datetime
from django.utils import timezone
from django.db.models import Q
from bookmarks.models import Registered
from users.telegram_utils import send_message_to_user

def send_event_reminders():
    now = timezone.now()
    one_hour_later = now + datetime.timedelta(hours=1)
    five_minutes_later = now + datetime.timedelta(minutes=5)

    events = Registered.objects.filter(
        Q(online__time_start__range=(one_hour_later.time(), five_minutes_later.time())) |
        Q(offline__time_start__range=(one_hour_later.time(), five_minutes_later.time())) |
        Q(attractions__time_start__range=(one_hour_later.time(), five_minutes_later.time())) |
        Q(for_visiting__time_start__range=(one_hour_later.time(), five_minutes_later.time()))
    ).select_related('user', 'online', 'offline', 'attractions', 'for_visiting')

    for event in events:
        if event.online:
            event_obj = event.online
        elif event.offline:
            event_obj = event.offline
        elif event.attractions:
            event_obj = event.attractions
        elif event.for_visiting:
            event_obj = event.for_visiting

        message = f"Напоминание: мероприятие '{event_obj.name}' начинается через час."
        send_message_to_user(event.user.telegram_id, message)
