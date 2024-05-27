from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import AdminRightRequest
from .telegram_utils import send_message_to_user
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=AdminRightRequest)
def notify_user_on_status_change(sender, instance, **kwargs):
    try:
        previous_instance = AdminRightRequest.objects.get(pk=instance.pk)
    except AdminRightRequest.DoesNotExist:
        previous_instance = None

    logger.info(f"Previous instance: {previous_instance}, Current instance: {instance}")

    if previous_instance and previous_instance.status == 'pending' and instance.status != 'pending':
        if instance.status == 'granted':
            message = f"Ваш запрос на админские права был одобрен. Причина: {instance.response}"
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
