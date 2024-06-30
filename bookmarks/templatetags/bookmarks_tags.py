from django import template
from bookmarks.models import Favorite, Registered

register = template.Library()

@register.simple_tag()
def user_favorites(request):
  return Favorite.objects.filter(user=request.user)

@register.simple_tag()
def user_registered(request):
  return Registered.objects.filter(user=request.user)