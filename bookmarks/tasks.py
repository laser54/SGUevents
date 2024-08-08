from datetime import timedelta
from django.utils.timezone import localtime, now as tz_now, get_current_timezone
from celery import shared_task
from django.db.models import Q
from bookmarks.models import Registered
from users.models import User
from users.telegram_utils import send_message_to_user_with_toggle_button, send_message_to_user_with_review_buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
        registered_event = Registered.objects.get(id=event_id)
        if registered_event.notifications_enabled:
            message = f"Напоминаем, что мероприятие '{event_name}' начнется через {timeframe}."
            if user.telegram_id:
                send_message_to_user_with_toggle_button(user.telegram_id, message, event_id, True)
            else:
                logger.warning(f"Пользователь {user.username} не имеет telegram_id, уведомление не отправлено.")
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except Registered.DoesNotExist:
        logger.error(f"Registered event with id {event_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

@shared_task
def send_review_request(event_id, user_id, event_name, event_type):
    try:
        user = User.objects.get(id=user_id)
        message = f"Мероприятие '{event_name}' завершилось. Пожалуйста, оставьте отзыв."

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "\U0000270D Оставить отзыв", "callback_data": f"leave_review_{event_type}_{event_id}"},
                    {"text": "В другой раз", "callback_data": f"review_later_{event_type}_{event_id}"}
                ]
            ]
        }

        if user.telegram_id:
            send_message_to_user_with_review_buttons(user.telegram_id, message, event_id, event_type, reply_markup)
        else:
            logger.warning(f"Пользователь {user.username} не имеет telegram_id, уведомление не отправлено.")
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending review request: {e}")

def determine_event_type(event):
    if event.online:
        return "online"
    elif event.offline:
        return "offline"
    elif event.attractions:
        return "attractions"
    elif event.for_visiting:
        return "for_visiting"
    else:
        raise ValueError("Unknown event type")

@shared_task
def schedule_notifications():
    now = round_to_minute(localtime(tz_now()))  # Используем локальное время и округляем до минуты
    previous_minute = now - timedelta(minutes=1)
    current_tz = get_current_timezone()

    timeframes = {
        '1 day': timedelta(days=1),
        '1 hour': timedelta(hours=1),
        '5 minutes': timedelta(minutes=5),
    }

    for timeframe, delta in timeframes.items():
        target_time = round_to_minute(now + delta)

        # Фильтрация зарегистрированных событий по связанным моделям
        registered_events = Registered.objects.filter(
            Q(online__start_datetime__lte=target_time, online__start_datetime__gt=previous_minute) |
            Q(offline__start_datetime__lte=target_time, offline__start_datetime__gt=previous_minute) |
            Q(attractions__start_datetime__lte=target_time, attractions__start_datetime__gt=previous_minute) |
            Q(for_visiting__start_datetime__lte=target_time, for_visiting__start_datetime__gt=previous_minute)
        )

        if registered_events.exists():
            for event in registered_events:
                if event.online:
                    start_datetime = round_to_minute(event.online.start_datetime.astimezone(current_tz))
                    event_name = event.online.name
                    end_datetime = event.online.end_datetime.astimezone(current_tz)
                elif event.offline:
                    start_datetime = round_to_minute(event.offline.start_datetime.astimezone(current_tz))
                    event_name = event.offline.name
                    end_datetime = event.offline.end_datetime.astimezone(current_tz)
                elif event.attractions:
                    start_datetime = round_to_minute(event.attractions.start_datetime.astimezone(current_tz))
                    event_name = event.attractions.name
                    end_datetime = event.attractions.end_datetime.astimezone(current_tz)
                elif event.for_visiting:
                    start_datetime = round_to_minute(event.for_visiting.start_datetime.astimezone(current_tz))
                    event_name = event.for_visiting.name
                    end_datetime = event.for_visiting.end_datetime.astimezone(current_tz)
                else:
                    continue

                event_type = determine_event_type(event)

                eta_time = start_datetime - delta

                if eta_time >= previous_minute:
                    send_notification.apply_async((event.id, event.user.id, event_name, timeframe), eta=now)
                else:
                    logger.warning(f"Время {eta_time} для события {event.id} уже прошло, уведомление не запланировано.")

                # Планирование уведомления о запросе отзыва
                review_eta_time = end_datetime + timedelta(minutes=1)
                if review_eta_time > now:
                    send_review_request.apply_async((event.id, event.user.id, event_name, event_type), eta=review_eta_time)
                else:
                    logger.warning(f"Время {review_eta_time} для события {event.id} уже прошло, запрос на отзыв не запланирован.")
