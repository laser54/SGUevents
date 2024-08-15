from django import template
from bookmarks.models import Favorite, Registered

register = template.Library()

@register.simple_tag()
def user_favorites(request):
  return Favorite.objects.filter(user=request.user)

@register.simple_tag()
def user_registered(request):
  return Registered.objects.filter(user=request.user)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def model_name(value):
    return value.__class__.__name__

# @register.filter
# def get_review(rev, res):
   

   