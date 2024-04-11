from django.db import models

class Events_online(models.Model):
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата' )
    time = models.TimeField(max_length=15, unique=False, blank=False, null=False, verbose_name='Время' )
    description = models.TextField(unique=False, blank=False, null=False, verbose_name='Описание')
    speakers = models.CharField(max_length=250, unique=False, blank=False, null=False, verbose_name='Спикеры')
    member = models.TextField(unique=False, blank=False, null=False, verbose_name='Участники')
    tags = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Теги')
    platform = models.CharField(max_length=50, unique=False, blank=False, null=False, verbose_name='Платформа')
    link = models.URLField(unique=False, blank=True, null=True, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/online', blank=True, null=True, verbose_name='Изображение')
    events_admin = models.TextField(unique=False, blank=False, null=False, verbose_name='Администратор')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')

    class Meta:
        db_table = 'Events_online'
        verbose_name = 'Онлайн мероприятие'
        verbose_name_plural = 'Онлайн'

    def __str__(self):
        return self.name
    
class Events_offline(models.Model):
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата' )
    time = models.TimeField(max_length=15, unique=False, blank=False, null=False, verbose_name='Время' )
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
    events_admin = models.TextField(unique=False, blank=False, null=False, verbose_name='Администратор')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    
    class Meta:
        db_table = 'Events_offline'
        verbose_name = 'Оффлайн мероприятие'
        verbose_name_plural = 'Оффлайн'

    def __str__(self):
        return self.name
