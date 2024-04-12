from django.contrib import admin

from events_cultural.models import Attractions, Events_for_visiting 

@admin.register(Attractions)
class AttractionsAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Events_for_visiting)
class Events_for_visitingAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}



