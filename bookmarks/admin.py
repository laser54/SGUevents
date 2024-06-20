from django.contrib import admin
from bookmarks.models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'added')
    search_fields = ('user__username', 'event_online__name', 'event_offline__name')
    list_filter = ('user', 'added')

    def event(self, obj):
        if obj.event_online:
            return obj.event_online.name
        elif obj.event_offline:
            return obj.event_offline.name
        return None
    event.short_description = 'Event'

admin.site.register(Favorite, FavoriteAdmin)
