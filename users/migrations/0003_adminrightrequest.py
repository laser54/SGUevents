from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_department_remove_user_department_id_user_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminRightRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(verbose_name='Основание')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('granted', 'Предоставлено'), ('denied', 'Отказано')], default='pending', max_length=20, verbose_name='Статус')),
                ('response', models.TextField(blank=True, null=True, verbose_name='Ответ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запрос на админские права',
                'verbose_name_plural': 'Запросы на админские права',
            },
        ),
    ]
