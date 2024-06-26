# Generated by Django 4.2.11 on 2024-07-01 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attractions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('date', models.DateField(max_length=10, verbose_name='Дата')),
                ('time_start', models.TimeField(verbose_name='Время начала')),
                ('time_end', models.TimeField(verbose_name='Время окончания')),
                ('description', models.TextField(verbose_name='Описание')),
                ('town', models.CharField(max_length=200, verbose_name='Город')),
                ('street', models.CharField(max_length=100, verbose_name='Улица')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('qr', models.FileField(blank=True, null=True, upload_to='', verbose_name='QR-код')),
                ('image', models.ImageField(blank=True, null=True, upload_to='events_available_images/offline', verbose_name='Изображение')),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='Рейтинг 1-10')),
                ('documents', models.FileField(blank=True, null=True, upload_to='', verbose_name='Документы')),
                ('category', models.CharField(default='Достопримечательности', max_length=30, verbose_name='Тип мероприятия')),
            ],
            options={
                'verbose_name': 'Достопримечательности',
                'verbose_name_plural': 'Достопримечательности',
                'db_table': 'attractions',
            },
        ),
        migrations.CreateModel(
            name='Events_for_visiting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('date', models.DateField(max_length=10, verbose_name='Дата')),
                ('time_start', models.TimeField(verbose_name='Время начала')),
                ('time_end', models.TimeField(verbose_name='Время окончания')),
                ('description', models.TextField(verbose_name='Описание')),
                ('member', models.TextField(verbose_name='Участники')),
                ('town', models.CharField(max_length=200, verbose_name='Город')),
                ('street', models.CharField(max_length=100, verbose_name='Улица')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Ссылка')),
                ('qr', models.FileField(blank=True, null=True, upload_to='', verbose_name='QR-код')),
                ('image', models.ImageField(blank=True, null=True, upload_to='events_available_images/offline', verbose_name='Изображение')),
                ('events_admin', models.CharField(max_length=100, verbose_name='Администратор')),
                ('place_limit', models.IntegerField(verbose_name='Количество мест')),
                ('place_free', models.IntegerField(verbose_name='Количество свободных мест')),
                ('documents', models.FileField(blank=True, null=True, upload_to='', verbose_name='Документы')),
                ('category', models.CharField(default='Доступные к посещению', max_length=30, verbose_name='Тип мероприятия')),
            ],
            options={
                'verbose_name': 'Доступные к посещению',
                'verbose_name_plural': 'Доступные к посещению',
                'db_table': 'Events_for_visiting',
            },
        ),
    ]
