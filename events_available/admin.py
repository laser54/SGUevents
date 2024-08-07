from django.contrib import admin

from events_available.models import Events_offline, Events_online

@admin.register(Events_online)
class Events_onlineAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	filter_horizontal = ('secret',)

@admin.register(Events_offline)
class Events_offlineAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	filter_horizontal = ('secret',)


