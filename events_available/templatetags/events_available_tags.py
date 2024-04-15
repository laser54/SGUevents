from django import template

from events_available.models import Events_offline, Events_online

register = template.Library()

@register.simple_tag()
def tag_online():
    return Events_online.objects.all()

@register.simple_tag()
def tag_offline():
    return Events_offline.objects.all()