from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from events_available.models import Events_offline, Events_online

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

# Настройка админ-панели для каждой модели
@admin.register(Events_online)
class Events_onlineAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('secret',)


@admin.register(Events_offline)
class Events_offlineAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('secret',)