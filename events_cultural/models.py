from django.db import models

class Attractions(models.Model):
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата' )
    time_start = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время начала' )
    time_end = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время окончания' )
    description = models.TextField(unique=False, blank=False, null=False, verbose_name='Описание')
    town = models.CharField(max_length=200, unique=False, blank=False, null=False, verbose_name='Город')
    street= models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Улица')
    link = models.URLField(unique=False, blank=False, null=False, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/offline', blank=True, null=True, verbose_name='Изображение')
    rating = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, blank=False, null=False, verbose_name='Рейтинг 1-10')
    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    category = "Достопримечательности"

    class Meta:
        db_table = 'attractions'
        verbose_name = 'Достопримечательности'
        verbose_name_plural = 'Достопримечательности'

    def __str__(self):
        return self.name
    
    def display_id(self):
        return f'{self.id:05}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.category = "Достопримечательности"
        super(Attractions, self).save(*args, **kwargs)


class Events_for_visiting(models.Model):
    name = models.CharField(max_length=150, unique=False, blank=False, null=False, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False, verbose_name='URL')
    date = models.DateField(max_length=10, unique=False, blank=False, null=False, verbose_name='Дата' )
    time_start = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время начала' )
    time_end = models.TimeField(unique=False, blank=False, null=False, verbose_name='Время окончания' )
    description = models.TextField(unique=False, blank=False, null=False, verbose_name='Описание')
    member = models.TextField(unique=False, blank=False, null=False, verbose_name='Участники')
    town = models.CharField(max_length=200, unique=False, blank=False, null=False, verbose_name='Город')
    street= models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Улица')
    link = models.URLField(unique=False, blank=True, null=True, verbose_name='Ссылка')
    qr = models.FileField(blank=True, null=True, verbose_name='QR-код')
    image = models.ImageField(upload_to='events_available_images/offline', blank=True, null=True, verbose_name='Изображение')
    events_admin = models.CharField(max_length=100, unique=False, blank=False, null=False, verbose_name='Администратор')
    place_limit = models.IntegerField(unique=False, blank=False, null=False, verbose_name='Количество мест')
    place_free = models.IntegerField(unique=False, blank=False, null=False, verbose_name='Количество свободных мест')
    category = "Доступные к посещению"

    documents = models.FileField(blank=True, null=True, verbose_name='Документы')
    
    class Meta:
        db_table = 'Events_for_visiting'
        verbose_name = 'Доступные к посещению'
        verbose_name_plural = 'Доступные к посещению'

    def __str__(self):
        return self.name
    
    def display_id(self):
        return f'{self.id:05}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.category = "Доступные к посещению"
        super(Events_for_visiting, self).save(*args, **kwargs)
