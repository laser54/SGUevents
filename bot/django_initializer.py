# django_initializer.py
import os
import django

def setup_django_environment():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")
    # В разработке вызываем setup, если приложения Django еще не загружены
    if os.getenv('DJANGO_ENV') == 'development' and not django.apps.apps.ready:
        django.setup()
