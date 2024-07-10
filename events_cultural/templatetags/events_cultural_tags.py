from django import template
from django.utils.http import urlencode

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)