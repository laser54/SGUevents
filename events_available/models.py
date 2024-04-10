from django.db import models

class Events_online(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    place = models.TextField(blank=True, null=True, verbose_name='Место')
    speakers = models.TextField(blank=True, null=True, verbose_name='Спикеры')
    image = models.ImageField(upload_to='#', blank=True, null=True, verbose_name='Изображение')
    
    class Meta:
        db_table = 'Events_online'
        verbose_name = 'Онлайн мероприятие'
        verbose_name_plural = 'Онлайн'

    def __str__(self):
        return self.name
    
class Events_offline(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    place = models.TextField(blank=True, null=True, verbose_name='Место')
    speakers = models.TextField(blank=True, null=True, verbose_name='Спикеры')
    image = models.ImageField(upload_to='#', blank=True, null=True, verbose_name='Изображение')
    
    class Meta:
        db_table = 'Events_offline'
        verbose_name = 'Оффлайн мероприятие'
        verbose_name_plural = 'Оффлайн'

    def __str__(self):
        return self.name
