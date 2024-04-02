from django.contrib import admin
from .models import User  # Импортируем модель пользователя

# Определяем класс администратора для настройки отображения модели в админ-панели
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'department_id', 'telegram_id')  # Поля, которые будут отображаться в списке объектов
    search_fields = ('first_name', 'last_name', 'middle_name', 'department_id', 'telegram_id')  # Поля, по которым будет работать поиск
    list_filter = ('department_id',)  # Фильтры справа по указанным полям

# Регистрируем модель User с настройками UserAdmin
admin.site.register(User, UserAdmin)
