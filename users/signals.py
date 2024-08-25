from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import AdminRightRequest
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting
from .telegram_utils import send_message_to_user
import logging
from users.middleware import CurrentUserMiddleware


logger = logging.getLogger(__name__)

# Уведомление о смене статуса AdminRightRequest
@receiver(pre_save, sender=AdminRightRequest)
def notify_user_on_status_change(sender, instance, **kwargs):
    try:
        previous_instance = AdminRightRequest.objects.get(pk=instance.pk)
    except AdminRightRequest.DoesNotExist:
        previous_instance = None

    logger.info(f"Previous instance: {previous_instance}, Current instance: {instance}")

    if previous_instance and previous_instance.status == 'pending' and instance.status != 'pending':
        if instance.status == 'granted':
            message = f"Ваш запрос на админские права был одобрен. Комментарий: {instance.response}"
        elif instance.status == 'denied':
            message = f"Ваш запрос на админские права был отклонен. Причина: {instance.response}"

        user_telegram_id = instance.user.telegram_id
        if user_telegram_id:
            logger.info(f"Отправка сообщения пользователю {instance.user.username} с telegram_id: {user_telegram_id}")
            send_message_to_user(user_telegram_id, message)
        else:
            logger.warning(f"У пользователя {instance.user.username} нет telegram_id")
    else:
        logger.info(f"Статус не изменен с 'pending' на другой или previous_instance отсутствует.")

# Уведомление авторов об изменениях в мероприятиях
@receiver(post_save, sender=Events_online)
@receiver(post_save, sender=Events_offline)
@receiver(post_save, sender=Attractions)
@receiver(post_save, sender=Events_for_visiting)
def notify_author_on_event_update(sender, instance, **kwargs):
    user = CurrentUserMiddleware.get_current_user()
    if user:
        if hasattr(user, 'telegram_id') and user.telegram_id:
            message = f"Изменения в мероприятие '{instance.name}' были успешно сохранены."
            send_message_to_user(user.telegram_id, message)
            logger.info(f"Уведомление об изменениях отправлено пользователю {user.username}")
        else:
            logger.warning(f"У пользователя {user.username} нет telegram_id")
    else:
        logger.warning("Пользователь, который вносит изменения, не был найден.")
