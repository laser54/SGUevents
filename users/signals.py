from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import AdminRightRequest
from .telegram_utils import send_message_to_user

@receiver(post_save, sender=AdminRightRequest)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    # Проверяем, что это не создание новой записи, а обновление существующей
    if created:
        return

    try:
        previous_instance = AdminRightRequest.objects.get(pk=instance.pk)
    except AdminRightRequest.DoesNotExist:
        previous_instance = None

    if previous_instance and previous_instance.status == 'pending' and instance.status != 'pending':
        if instance.status == 'granted':
            message = f"Ваш запрос на админские права был одобрен. Причина: {instance.response}"
        elif instance.status == 'denied':
            message = f"Ваш запрос на админские права был отклонен. Причина: {instance.response}"

        user_telegram_id = instance.user.telegram_id  # Теперь используем telegram_id напрямую из модели User
        if user_telegram_id:
            send_message_to_user(user_telegram_id, message)
        else:
            print(f"Ошибка: У пользователя {instance.user.username} нет telegram_id")
