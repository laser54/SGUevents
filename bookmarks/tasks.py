from datetime import timedelta
from django.utils.timezone import localtime, now as tz_now, get_current_timezone
from celery import shared_task
from bookmarks.models import Registered
from users.telegram_utils import send_message_to_user
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification(event_id, user_id, timeframe):
    try:
        registered_event = Registered.objects.get(id=event_id)
        user = registered_event.user
        event_name = registered_event.online.name if registered_event.online else (
            registered_event.offline.name if registered_event.offline else (
                registered_event.attractions.name if registered_event.attractions else (
                    registered_event.for_visiting.name if registered_event.for_visiting else "Неизвестное мероприятие"
                )
            )
        )
        message = f"Напоминаем, что мероприятие '{event_name}' начнется через {timeframe}."
        if user.telegram_id:
            send_message_to_user(user.telegram_id, message)
            logger.info(f"Отправлено уведомление пользователю {user.username} с telegram_id: {user.telegram_id} о мероприятии {event_name}.")
        else:
            logger.warning(f"Пользователь {user.username} не имеет telegram_id, уведомление не отправлено.")
    except Registered.DoesNotExist:
        logger.error(f"Registered event with id {event_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

@shared_task
def schedule_notifications():
    now = localtime(tz_now())  # Используем локальное время
    logger.info(f"Текущее локальное время: {now}")
    timeframes = {
        '1 day': timedelta(days=1),
        '1 hour': timedelta(hours=1),
        '5 minutes': timedelta(minutes=5),
    }

    for timeframe, delta in timeframes.items():
        target_time = now + delta
        logger.info(f"Проверка временного интервала: {timeframe}")
        logger.info(f"Целевое время для {timeframe}: {target_time}")

        registered_events = Registered.objects.filter(start_datetime__lte=target_time, start_datetime__gt=now)
        if registered_events.exists():
            logger.info(f"Найдено зарегистрированных событий для {timeframe}: {registered_events.count()}")
            for event in registered_events:
                eta_time = localtime(event.start_datetime - delta, get_current_timezone())
                logger.info(f"Проверка события {event.id} с началом в {event.start_datetime}, ETA время: {eta_time}")
                if eta_time > now:
                    send_notification.apply_async((event.id, event.user.id, timeframe), eta=eta_time)
                    logger.info(f"Запланировано уведомление для события {event.id} пользователю {event.user.id} в {eta_time} о мероприятии запланированном на {event.start_datetime}.")
                else:
                    logger.warning(f"Время {eta_time} для события {event.id} уже прошло, уведомление не запланировано.")
        else:
            logger.info(f"Нет зарегистрированных событий для уведомления за {timeframe}.")
