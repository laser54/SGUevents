import uuid
from django.db import models

class Events_online(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный ID')
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата' )
    time_start = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время начала' )
    time_end = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время окончания' )
    description = models.TextField(unique=False, blank=False, null=False, verbose_name='Описание')
    speakers = models.CharField(max_length=250, unique=False, blank=False, null=False, verbose_name='Спикеры')
    member = models.TextField(unique=False, blank=False, null=False, verbose_name='Участники')
    tags = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Теги')
    platform = models.CharField(max_length=50, unique=False, blank=False, null=False, verbose_name='Платформа')
    link = models.URLField(unique=False, blank=False, null=False, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/online', blank=True, null=True, verbose_name='Изображение')
    events_admin = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Администратор')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    const_category = 'Онлайн'
    category = models.CharField(default=const_category, max_length=30, unique=False, blank=False, null=False, verbose_name='Тип мероприятия')

    class Meta:
        db_table = 'Events_online'
        verbose_name = 'Онлайн мероприятие'
        verbose_name_plural = 'Онлайн'

    def __str__(self):
        return self.name
    
    def display_id(self):
        return f'{self.id:05}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.category = "Онлайн"
        super(Events_online, self).save(*args, **kwargs)
    
class Events_offline(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Уникальный ID')
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата' )
    time_start = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время начала' )
    time_end = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время окончания' )
    description = models.TextField(unique=False, blank=False, null=False, verbose_name='Описание')
    speakers = models.CharField(max_length=250, unique=False, blank=False, null=False, verbose_name='Спикеры')
    member = models.TextField(unique=False, blank=False, null=False, verbose_name='Участники')
    tags = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Теги')
    town = models.CharField(max_length=200, unique=False, blank=False, null=False, verbose_name='Город')
    street= models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Улица')
    cabinet = models.CharField(max_length=50, unique=False, blank=False, null=False, verbose_name='Кабинет')
    link = models.URLField(unique=False, blank=True, null=True, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/offline', blank=True, null=True, verbose_name='Изображение')
    events_admin = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Администратор')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    const_category = 'Оффлайн'
    category = models.CharField(default=const_category, max_length=30, unique=False, blank=False, null=False, verbose_name='Тип мероприятия')
    
    class Meta:
        db_table = 'Events_offline'
        verbose_name = 'Оффлайн мероприятие'
        verbose_name_plural = 'Оффлайн'

    def __str__(self):
        return self.name
    
    def display_id(self):
        return f'{self.id:05}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.category = "Оффлайн"
        super(Events_offline, self).save(*args, **kwargs)