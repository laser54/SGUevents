import uuid
from django.db import models
from datetime import datetime
from django.utils.timezone import make_aware, get_default_timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from users.models import User

class Attractions(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный ID')
    name = models.CharField(max_length=150, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=False, verbose_name='URL')
    date = models.DateField(max_length=10, blank=False, verbose_name='Дата')
    time_start = models.TimeField(blank=False, null=False, verbose_name='Время начала')
    time_end = models.TimeField(blank=False, null=False, verbose_name='Время окончания')
    description = models.TextField(blank=False, null=False, verbose_name='Описание')
    town = models.CharField(max_length=200, blank=False, verbose_name='Город')
    street = models.CharField(max_length=100, blank=False, verbose_name='Улица')
    link = models.URLField(blank=False, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/offline', blank=True, null=True, verbose_name='Изображение')
    rating = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, blank=False, verbose_name='Рейтинг 1-10')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    const_category = 'Достопримечательности'
    category = models.CharField(default=const_category, max_length=30, blank=False, verbose_name='Тип мероприятия')
    reviews = GenericRelation('Review', related_query_name='attraction_reviews')
    start_datetime = models.DateTimeField(editable=False, null=True, blank=True, verbose_name='Дата и время начала')

    class Meta:
        db_table = 'attractions'
        verbose_name = 'Достопримечательности'
        verbose_name_plural = 'Достопримечательности'

    def __str__(self):
        return self.name

    def display_id(self):
        return f'{self.id:05}'

    def save(self, *args, **kwargs):
        combined_datetime = datetime.combine(self.date, self.time_start)
        self.start_datetime = make_aware(combined_datetime, timezone=get_default_timezone())
        super(Attractions, self).save(*args, **kwargs)

class Events_for_visiting(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный ID')
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата')
    time_start = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время начала')
    time_end = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время окончания')
    description = models.TextField(unique=False, blank=False, null=False, verbose_name='Описание')
    member = models.TextField(unique=False, blank=False, null=False, verbose_name='Участники')
    town = models.CharField(max_length=200, unique=False, blank=False, null=False, verbose_name='Город')
    street = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Улица')
    link = models.URLField(unique=False, blank=True, null=True, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/offline', blank=True, null=True, verbose_name='Изображение')
    events_admin = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Администратор')
    place_limit = models.IntegerField(unique=False, blank=False, null=False, verbose_name='Количество мест')
    place_free = models.IntegerField(unique=False, blank=False, null=False, verbose_name='Количество свободных мест')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    const_category = 'Доступные к посещению'
    category = models.CharField(default=const_category, max_length=30, unique=False, blank=False, null=False, verbose_name='Тип мероприятия')
    reviews = GenericRelation('Review', related_query_name='visiting_reviews')
    start_datetime = models.DateTimeField(editable=False, null=True, blank=True, verbose_name='Дата и время начала')

    class Meta:
        db_table = 'Events_for_visiting'
        verbose_name = 'Доступные к посещению'
        verbose_name_plural = 'Доступные к посещению'

    def __str__(self):
        return self.name

    def display_id(self):
        return f'{self.id:05}'

    def save(self, *args, **kwargs):
        combined_datetime = datetime.combine(self.date, self.time_start)
        self.start_datetime = make_aware(combined_datetime, timezone=get_default_timezone())
        super(Events_for_visiting, self).save(*args, **kwargs)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
    object_id = models.PositiveIntegerField(default=1)
    event = GenericForeignKey('content_type', 'object_id')
    comment = models.TextField(verbose_name='Комментарий')
    date_submitted = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.date_submitted.strftime("%d.%m.%Y %H:%M")} Отзыв от {self.user.username} на {self.event}'

    def formatted_date(self):
        return self.date_submitted.strftime("%d.%m.%y %H:%M")
