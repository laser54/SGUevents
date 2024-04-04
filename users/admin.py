from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Custom fields'), {'fields': ('department_id', 'telegram_id')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Custom fields'), {'fields': ('department_id', 'telegram_id')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'middle_name', 'department_id', 'telegram_id', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'middle_name', 'email', 'department_id', 'telegram_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'department_id')

admin.site.register(User, UserAdmin)
