# Generated by Django 4.2.11 on 2024-06-21 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events_cultural', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_atr', models.ForeignKey(db_column='event_atr_id', on_delete=django.db.models.deletion.CASCADE, to='events_cultural.attractions', verbose_name='Достопр')),
            ],
            options={
                'verbose_name': 'Достопримечательности',
                'verbose_name_plural': 'Достопримечательности',
                'db_table': 'AllEvents',
            },
        ),
    ]
