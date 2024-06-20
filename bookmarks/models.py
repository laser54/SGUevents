from django.conf import settings
from django.db import models
from events_available.models import Events_online, Events_offline

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_online = models.ForeignKey(Events_online, null=True, blank=True, on_delete=models.CASCADE)
    event_offline = models.ForeignKey(Events_offline, null=True, blank=True, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event_online', 'event_offline')

    def __str__(self):
        if self.event_online:
            return f'Favorite: {self.event_online.name}'
        else:
            return f'Favorite: {self.event_offline.name}'
