import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.timezone import make_aware, get_default_timezone
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.telegram_utils import send_message_to_user_with_toggle_button
import logging

logger = logging.getLogger(__name__)

class Favorite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1, verbose_name="Пользователь")
    online = models.ForeignKey(to=Events_online, on_delete=models.CASCADE, verbose_name="Онлайн", null=True, blank=True)
    offline = models.ForeignKey(to=Events_offline, on_delete=models.CASCADE, verbose_name="Оффлайн", null=True, blank=True)
    attractions = models.ForeignKey(to=Attractions, on_delete=models.CASCADE, verbose_name="Достопримечательности", null=True, blank=True)
    for_visiting = models.ForeignKey(to=Events_for_visiting, on_delete=models.CASCADE, verbose_name="Доступные для посещения", null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранные"
        verbose_name_plural = "Избранные"

    def __str__(self):
        try:
            return f'Избранные {self.user.middle_name} | Мероприятие {self.online.name} | Тип {self.online.category}'
        except:
            try:
                return f'Избранные {self.user.middle_name} | Мероприятие {self.offline.name} | Тип {self.offline.category}'
            except:
                try:
                    return f'Избранные {self.user.middle_name} | Мероприятие {self.attractions.name} | Тип {self.attractions.category}'
                except:
                    return f'Избранные {self.user.middle_name} | Мероприятие {self.for_visiting.name} | Тип {self.for_visiting.category}'


class Registered(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Уникальный ID")  # Removed unique=True
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    online = models.ForeignKey(to=Events_online, on_delete=models.CASCADE, verbose_name="Онлайн", null=True, blank=True)
    offline = models.ForeignKey(to=Events_offline, on_delete=models.CASCADE, verbose_name="Оффлайн", null=True, blank=True)
    attractions = models.ForeignKey(to=Attractions, on_delete=models.CASCADE, verbose_name="Достопримечательности", null=True, blank=True)
    for_visiting = models.ForeignKey(to=Events_for_visiting, on_delete=models.CASCADE, verbose_name="Доступные для посещения", null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    notifications_enabled = models.BooleanField(default=True, verbose_name="Уведомления включены")

    class Meta:
        verbose_name = "Зарегистрированные"
        verbose_name_plural = "Зарегистрированные"

    def __str__(self):
        try:
            return f'Зарегистрированные {self.user.middle_name} | Мероприятие {self.online.name} | Тип {self.online.category}'
        except:
            try:
                return f'Зарегистрированные {self.user.middle_name} | Мероприятие {self.offline.name} | Тип {self.offline.category}'
            except:
                try:
                    return f'Зарегистрированные {self.user.middle_name} | Мероприятие {self.attractions.name} | Тип {self.attractions.category}'
                except:
                    return f'Зарегистрированные {self.user.middle_name} | Мероприятие {self.for_visiting.name} | Тип {self.for_visiting.category}'


@receiver(post_save, sender=Registered)
def notify_user_on_registration(sender, instance, created, **kwargs):
    if created:
        event_name = instance.online.name if instance.online else (
            instance.offline.name if instance.offline else (
                instance.attractions.name if instance.attractions else instance.for_visiting.name))
        message = f"Вы зарегистрировались на мероприятие: {event_name}."
        user_telegram_id = instance.user.telegram_id
        if user_telegram_id:
            logger.info(f"Отправка сообщения о регистрации пользователю {instance.user.username} с telegram_id: {user_telegram_id}")
            send_message_to_user_with_toggle_button(user_telegram_id, message, instance.id, instance.notifications_enabled)
        else:
            logger.warning(f"У пользователя {instance.user.username} нет telegram_id")
