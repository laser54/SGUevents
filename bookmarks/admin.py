from django.contrib import admin

from bookmarks.models import Favorite, Registered

admin.site.register(Favorite)
admin.site.register(Registered)

