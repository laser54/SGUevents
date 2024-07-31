import os
import sys
import django
from django.utils.timezone import localtime, get_current_timezone, make_naive
from datetime import datetime

# Задайте путь к вашему проекту Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")
django.setup()

from bookmarks.models import Registered

def check_events():
    events = Registered.objects.all()
    current_tz = get_current_timezone()

    print("Список зарегистрированных событий:")
    for event in events:
        if event.start_datetime:
            local_dt = localtime(event.start_datetime, current_tz)
            naive_dt = make_naive(event.start_datetime, current_tz)
            print(f"ID: {event.id}")
            print(f"Пользователь: {event.user.username}")
            print(f"Начало (локальное время): {local_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            print(f"Начало (наивное время): {naive_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Оригинальное время (UTC): {event.start_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            print("-" * 50)
        else:
            print(f"ID: {event.id} не имеет start_datetime")

if __name__ == "__main__":
    check_events()
