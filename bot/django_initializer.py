import os
import django
from django.core.wsgi import get_wsgi_application

def setup_django_environment():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")
    if not django.apps.apps.ready:
        if os.getenv('DJANGO_ENV') == 'production':
            # В продакшене используем get_wsgi_application, которое делает setup автоматически
            return get_wsgi_application()
        else:
            # В разработке просто делаем setup
            django.setup()
