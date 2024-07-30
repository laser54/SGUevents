# bookmarks/tasks.py
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, is_naive, localtime
from celery import shared_task
from bookmarks.models import Registered
from users.telegram_utils import send_message_to_user
import logging

logger = logging.getLogger(__name__)

def make_aware_if_naive(dt):
    return make_aware(dt) if is_naive(dt) else dt

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
            logger.info(
                f"Отправлено уведомление пользователю {user.username} с telegram_id: {user.telegram_id} о мероприятии {event_name}.")
        else:
            logger.warning(f"Пользователь {user.username} не имеет telegram_id, уведомление не отправлено.")
    except Registered.DoesNotExist:
        logger.error(f"Registered event with id {event_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

@shared_task
def schedule_notifications():
    now = make_aware_if_naive(datetime.now())
    timeframes = {
        '1 day': timedelta(days=1),
        '1 hour': timedelta(hours=1),
        '5 minutes': timedelta(minutes=5),
    }

    for timeframe, delta in timeframes.items():
        logger.info(f"Проверка временного интервала: {timeframe}")
        target_time = now + delta
        logger.info(f"Целевое время для {timeframe}: {target_time}")

        future_events = Registered.objects.filter(start_datetime__gt=now)

        if future_events.exists():
            logger.info(f"Найдено зарегистрированных событий для {timeframe}: {future_events.count()}")
            for event in future_events:
                notification_time = make_aware_if_naive(event.start_datetime - delta)
                if notification_time > now:
                    # Проверяем, есть ли уже запланированное уведомление
                    existing_tasks = [task for task in Registered.objects.filter(start_datetime=event.start_datetime)]
                    if not existing_tasks:
                        send_notification.apply_async((event.id, event.user.id, timeframe), eta=notification_time)
                        logger.info(f"Запланировано уведомление для события {event.id} пользователю {event.user.username} в {notification_time} о мероприятии запланированном на {event.start_datetime}.")
                    else:
                        logger.info(f"Уведомление для события {event.id} уже запланировано.")
                else:
                    logger.info(f"Время {notification_time} для события {event.id} уже прошло, уведомление не запланировано.")
        else:
            logger.info(f"Нет зарегистрированных событий для уведомления за {timeframe}.")

    # Снимаем запланированные задачи, если пользователь отменил регистрацию или изменил время события
    for event in future_events:
        for timeframe, delta in timeframes.items():
            notification_time = make_aware_if_naive(event.start_datetime - delta)
            if notification_time <= now:
                send_notification.apply_async((event.id, event.user.id, timeframe), eta=notification_time)
                logger.info(f"Запланированное уведомление для события {event.id} было удалено.")
