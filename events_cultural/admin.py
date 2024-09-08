from django.contrib import admin

from events_cultural.models import Attractions, Events_for_visiting
from django.contrib.auth import get_user_model

User = get_user_model()

# Проверка группы
def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

class RestrictedAdminMixin:

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # все для суперюзера
        # мероприятия, где польз админ
        return qs.filter(events_admin=request.user.pk)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            # редактирование если польз администратор мероприятия
            return obj.events_admin == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            # удаление если польз администратор мероприятия
            return obj.events_admin == request.user
        return super().has_delete_permission(request, obj)

@admin.register(Attractions)
class AttractionsAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('events_admin',)

@admin.register(Events_for_visiting)
class Events_for_visitingAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('events_admin', 'member')



