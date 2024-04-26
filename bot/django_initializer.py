import os
import django

def setup_django_environment():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")
    if not hasattr(django, 'apps'):
        django.setup()