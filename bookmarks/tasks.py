from datetime import timedelta
from django.utils.timezone import localtime, now as tz_now, get_current_timezone
from celery import shared_task
from django.db.models import Q
from bookmarks.models import Registered
from users.models import User
from users.telegram_utils import send_message_to_user
import logging

logger = logging.getLogger(__name__)

def round_to_minute(dt):
    """Округление времени до ближайшей минуты"""
    if dt.second >= 30:
        dt += timedelta(minutes=1)
    return dt.replace(second=0, microsecond=0)

@shared_task
def send_notification(event_id, user_id, event_name, timeframe):
    try:
        user = User.objects.get(id=user_id)
        message = f"Напоминаем, что мероприятие '{event_name}' начнется через {timeframe}."
        if user.telegram_id:
            send_message_to_user(user.telegram_id, message)
            logger.info(f"Отправлено уведомление пользователю {user.username} с telegram_id: {user.telegram_id} о мероприятии {event_name}.")
        else:
            logger.warning(f"Пользователь {user.username} не имеет telegram_id, уведомление не отправлено.")
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

@shared_task
def schedule_notifications():
    now = round_to_minute(localtime(tz_now()))  # Используем локальное время и округляем до минуты
    previous_minute = now - timedelta(minutes=1)
    current_tz = get_current_timezone()
    logger.info(f"Текущее локальное время: {now}")
    timeframes = {
        '1 day': timedelta(days=1),
        '1 hour': timedelta(hours=1),
        '5 minutes': timedelta(minutes=5),
    }

    for timeframe, delta in timeframes.items():
        target_time = round_to_minute(now + delta)
        logger.info(f"Проверка временного интервала: {timeframe}")
        logger.info(f"Целевое время для {timeframe}: {target_time}")

        # Фильтрация зарегистрированных событий по связанным моделям
        registered_events = Registered.objects.filter(
            Q(online__start_datetime__lte=target_time, online__start_datetime__gt=previous_minute) |
            Q(offline__start_datetime__lte=target_time, offline__start_datetime__gt=previous_minute) |
            Q(attractions__start_datetime__lte=target_time, attractions__start_datetime__gt=previous_minute) |
            Q(for_visiting__start_datetime__lte=target_time, for_visiting__start_datetime__gt=previous_minute)
        )

        if registered_events.exists():
            logger.info(f"Найдено зарегистрированных событий для {timeframe}: {registered_events.count()}")
            for event in registered_events:
                if event.online:
                    start_datetime = round_to_minute(event.online.start_datetime.astimezone(current_tz))
                    event_name = event.online.name
                elif event.offline:
                    start_datetime = round_to_minute(event.offline.start_datetime.astimezone(current_tz))
                    event_name = event.offline.name
                elif event.attractions:
                    start_datetime = round_to_minute(event.attractions.start_datetime.astimezone(current_tz))
                    event_name = event.attractions.name
                elif event.for_visiting:
                    start_datetime = round_to_minute(event.for_visiting.start_datetime.astimezone(current_tz))
                    event_name = event.for_visiting.name
                else:
                    continue

                eta_time = start_datetime - delta
                logger.info(f"Проверка события {event.id} с началом в {start_datetime}, ETA время: {eta_time}")

                if eta_time >= previous_minute:
                    send_notification.apply_async((event.id, event.user.id, event_name, timeframe), eta=now)
                    logger.info(f"Запланировано уведомление для события {event.id} пользователю {event.user.id} в {now} о мероприятии запланированном на {start_datetime}.")
                else:
                    logger.warning(f"Время {eta_time} для события {event.id} уже прошло, уведомление не запланировано.")
        else:
            logger.info(f"Нет зарегистрированных событий для уведомления за {timeframe}.")
