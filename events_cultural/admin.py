from django.contrib import admin
from django.utils.timezone import localtime
from pytz import timezone as pytz_timezone
from events_cultural.models import Attractions, Events_for_visiting, Review
from django.contrib.auth import get_user_model

User = get_user_model()

# Проверяем, принадлежит ли пользователь к определенной группе
def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

class RestrictedAdminMixin:
    """
    Миксин для ограничения прав редактирования и удаления объектов в зависимости от того,
    является ли пользователь администратором мероприятия.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Суперпользователь видит все объекты
        # Пользователь видит только те мероприятия, где он администратор
        return qs.filter(events_admin=request.user.pk)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            # Разрешаем редактирование только если пользователь администратор мероприятия
            return obj.events_admin == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            # Разрешаем удаление только если пользователь администратор мероприятия
            return obj.events_admin == request.user
        return super().has_delete_permission(request, obj)

@admin.register(Attractions)
class AttractionsAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Events_for_visiting)
class Events_for_visitingAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('formatted_date_submitted', 'user', 'event', 'comment')

    def formatted_date_submitted(self, obj):
        local_time = localtime(obj.date_submitted, pytz_timezone('Asia/Novosibirsk'))
        return local_time.strftime('%d.%m.%Y %H:%M')

    formatted_date_submitted.short_description = 'Дата отправки'
    
admin.site.register(Review, ReviewAdmin)


