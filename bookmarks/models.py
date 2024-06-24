from django.db import models
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting
from users.models import  User

class Favorite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    online = models.ForeignKey(to=Events_online, on_delete=models.CASCADE, verbose_name="Онлайн", null=True, blank=True)
    offline = models.ForeignKey(to=Events_offline, on_delete=models.CASCADE, verbose_name="Оффлайн", null=True, blank=True)
    attractions = models.ForeignKey(to=Attractions, on_delete=models.CASCADE, verbose_name="Достопримечательности", null=True, blank=True)
    for_visiting = models.ForeignKey(to=Events_for_visiting, on_delete=models.CASCADE, verbose_name="Доступные для посещения", null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    
    class Meta:
        verbose_name = "Избранные"
        verbose_name_plural = "Избранные"
    
    def __str__(self):
        return f'Избранные {self.user.middle_name} | Мероприятие {self.online.name} | Тип {self.online.category}'
