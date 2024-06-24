from django import template
from bookmarks.models import Favorite

register = template.Library()

@register.simple_tag()
def user_favorites(request):
  return Favorite.objects.filter(user=request.user)