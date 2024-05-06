from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from events_available.models import Events_offline, Events_online
from events_cultural.models import Events_for_visiting
    
class AllEvents(models.Model):
	event = models.OneToOneField('events_available.Events_online', on_delete=models.CASCADE, null=True)

@receiver(post_save, sender=Events_online)
def create_all_events_online(sender, instance, created, **kwargs): 
	if created:
		AllEvents.objects.create(event=instance)

@receiver(post_save, sender=Events_offline)
def create_all_events_offline(sender, instance, created, **kwargs):
	if created:
		AllEvents.objects.create(event=instance)
	

