from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string
from transliterate import translit, exceptions


class CustomUserManager(BaseUserManager):
    def transliterate_username(self, last_name, first_name, middle_name=''):
        transliterated = ''
        try:
            if last_name:
                transliterated += translit(last_name, 'ru', reversed=True)
            if first_name:
                transliterated += translit(first_name[0], 'ru', reversed=True)
            if middle_name:
                transliterated += translit(middle_name[0], 'ru', reversed=True)
        except exceptions.LanguageDetectionError:
            transliterated = last_name + first_name[0] + (middle_name[0] if middle_name else '')

        base_username = transliterated
        counter = 1
        while self.model.objects.filter(username=transliterated).exists():
            transliterated = f"{base_username}{counter}"
            counter += 1
        return transliterated

    def create_user(self, email, first_name, last_name, middle_name='', department_id=666, telegram_id=None,
                    password=None, **extra_fields):
        username = extra_fields.pop('username', self.transliterate_username(last_name, first_name, middle_name))

        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            department_id=department_id,  # Используется переданное значение или значение по умолчанию
            telegram_id=telegram_id,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        # Предполагаем, что `first_name` и `last_name` передаются в `extra_fields`
        first_name = extra_fields.pop('first_name', 'Admin')
        last_name = extra_fields.pop('last_name', 'User')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Пример использования email и password, предполагаем, что они передаются через extra_fields
        email = extra_fields.pop('email')
        # Задаем длину пароля 8 символов
        password = extra_fields.pop('password', get_random_string(8))

        return self.create_user(email=email, first_name=first_name, last_name=last_name, password=password,
                                **extra_fields)


class User(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    department_id = models.IntegerField(verbose_name='ID отдела', default=666)
    telegram_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='Telegram ID')

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
