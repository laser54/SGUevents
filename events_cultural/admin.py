from django.contrib import admin
from django.utils.timezone import localtime
from pytz import timezone as pytz_timezone
from events_cultural.models import Attractions, Events_for_visiting, Review

@admin.register(Attractions)
class AttractionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('secret',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(events_admin=request.user.username)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.events_admin == request.user.username
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.events_admin == request.user.username
        return super().has_delete_permission(request, obj)

@admin.register(Events_for_visiting)
class Events_for_visitingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('secret',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(events_admin=request.user.username)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.events_admin == request.user.username
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.events_admin == request.user.username
        return super().has_delete_permission(request, obj)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('formatted_date_submitted', 'user', 'event', 'comment')

    def formatted_date_submitted(self, obj):
        local_time = localtime(obj.date_submitted, pytz_timezone('Asia/Novosibirsk'))
        return local_time.strftime('%d.%m.%Y %H:%M')

    formatted_date_submitted.short_description = 'Дата отправки'
    
admin.site.register(Review, ReviewAdmin)


