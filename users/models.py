from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from transliterate import translit, exceptions


class CustomUserManager(BaseUserManager):
    def transliterate_username(self, last_name, first_name, middle_name=''):
        transliterated = ''
        try:
            transliterated = translit(last_name, 'ru', reversed=True)
            transliterated += translit(first_name[0], 'ru', reversed=True) if first_name else ''
            transliterated += translit(middle_name[0], 'ru', reversed=True) if middle_name else ''
        except exceptions.LanguageDetectionError:
            transliterated = last_name + (first_name[0] if first_name else '') + (middle_name[0] if middle_name else '')

        base_username = transliterated
        counter = 1
        while self.model.objects.filter(username=transliterated).exists():
            transliterated = f"{base_username}{counter}"
            counter += 1

        return transliterated

    def create_user(self, email=None, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        else:
            email = None  # Убедитесь, что email может быть None, если не предоставлен
        password = get_random_string(8) if password is None else password
        first_name = extra_fields.pop('first_name', '')
        last_name = extra_fields.pop('last_name', '')
        middle_name = extra_fields.pop('middle_name', '')
        department_id = extra_fields.pop('department_id', None)
        telegram_id = extra_fields.pop('telegram_id', None)

        username = extra_fields.pop('username', None) or self.transliterate_username(last_name, first_name, middle_name)

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            department_id=department_id,
            telegram_id=telegram_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('department_id', 1)  # Убеждаемся, что это значение применяется
        extra_fields.setdefault('telegram_id', 'default_telegram_id')  # Можете установить другое значение по умолчанию

        if not email:
            raise ValueError('The Email must be set for superuser')
        if password is None:
            raise ValueError('Superuser must have a password')

        email = self.normalize_email(email)
        user = self.create_user(email, password, **extra_fields)

        user.save(using=self._db)
        return user


class User(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    department_id = models.IntegerField(verbose_name='ID отдела', default=666)
    telegram_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='Telegram ID')
    email = models.EmailField('email address', blank=True, null=True, unique=True)  # Добавлено blank=True, null=True

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
