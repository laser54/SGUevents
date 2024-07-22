import datetime
import logging
from django.utils import timezone
from bookmarks.models import Registered
from users.telegram_utils import send_message_to_user

logger = logging.getLogger(__name__)


def send_event_reminders():
    now = timezone.now()
    time_intervals = [
        datetime.timedelta(days=1),
        datetime.timedelta(hours=1),
        datetime.timedelta(minutes=5),
    ]

    for interval in time_intervals:
        reminder_time = now + interval
        # Увеличиваем временное окно для фильтрации
        start_time_window = reminder_time - datetime.timedelta(minutes=1)
        end_time_window = reminder_time + datetime.timedelta(minutes=1)

        events = Registered.objects.filter(
            start_datetime__gte=start_time_window,
            start_datetime__lt=end_time_window
        )

        logger.info(f"Interval: {interval}, Reminder time: {reminder_time}, Events found: {events.count()}")

        for event in events:
            user = event.user
            if user.telegram_id:
                message = f'Ваше событие "{event.online.name}" начнется через {interval}.'
                send_message_to_user(user.telegram_id, message)
                logger.info(
                    f"Отправлено сообщение пользователю {user.username} о событии {event.online.name} через {interval}.")
            else:
                logger.warning(f"User {user.username} has no telegram_id.")
