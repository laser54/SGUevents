from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    department_id = models.IntegerField(verbose_name='ID отдела')
    telegram_id = models.CharField(max_length=100, unique=True, verbose_name='Telegram ID')

    def __str__(self):
        # Возвращает полное имя пользователя, включая отчество, если оно указано
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}" if self.middle_name else f"{self.first_name} {self.last_name}"
        return full_name.strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
