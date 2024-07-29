# test_notifications.py

import os
import django
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, get_current_timezone
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")
django.setup()

from bookmarks.models import Registered
from events_available.models import Events_online
from users.models import User
from bookmarks.tasks import schedule_notifications, send_notification

# Получаем текущего пользователя для теста и обновляем его telegram_id
user = User.objects.first()
user.telegram_id = "1349308"
user.save()

# Текущее время с временной зоной
now = make_aware(datetime.now(), get_current_timezone())

# Создаем тестовые события с уникальными slug и временными метками с учетом временной зоны
event_online_day = Events_online.objects.create(
    unique_id=uuid.uuid4(),
    name="Test Event Online 1 Day",
    slug=f"test-event-online-day-{uuid.uuid4()}",
    date=(now + timedelta(days=1)).date(),
    time_start=(now + timedelta(days=1)).time(),
    time_end=(now + timedelta(days=1, hours=2)).time(),
    description="Description for Test Event Online 1 Day",
    speakers="Speaker 1, Speaker 2",
    member="Member 1, Member 2",
    tags="tag1, tag2",
    platform="Zoom",
    link="http://example.com",
    events_admin="Admin 1",
)

event_online_hour = Events_online.objects.create(
    unique_id=uuid.uuid4(),
    name="Test Event Online 1 Hour",
    slug=f"test-event-online-hour-{uuid.uuid4()}",
    date=now.date(),
    time_start=(now + timedelta(hours=1)).time(),
    time_end=(now + timedelta(hours=2)).time(),
    description="Description for Test Event Online 1 Hour",
    speakers="Speaker 1, Speaker 2",
    member="Member 1, Member 2",
    tags="tag1, tag2",
    platform="Zoom",
    link="http://example.com",
    events_admin="Admin 1",
)

event_online_minutes = Events_online.objects.create(
    unique_id=uuid.uuid4(),
    name="Test Event Online 5 Minutes",
    slug=f"test-event-online-minutes-{uuid.uuid4()}",
    date=now.date(),
    time_start=(now + timedelta(minutes=5)).time(),
    time_end=(now + timedelta(hours=1)).time(),
    description="Description for Test Event Online 5 Minutes",
    speakers="Speaker 1, Speaker 2",
    member="Member 1, Member 2",
    tags="tag1, tag2",
    platform="Zoom",
    link="http://example.com",
    events_admin="Admin 1",
)

# Регистрируем пользователя на тестовые события
reg_day = Registered.objects.create(
    user=user,
    online=event_online_day,
    start_datetime=make_aware(event_online_day.start_datetime, get_current_timezone())
)
reg_hour = Registered.objects.create(
    user=user,
    online=event_online_hour,
    start_datetime=make_aware(event_online_hour.start_datetime, get_current_timezone())
)
reg_minutes = Registered.objects.create(
    user=user,
    online=event_online_minutes,
    start_datetime=make_aware(event_online_minutes.start_datetime, get_current_timezone())
)

# Запускаем функцию для проверки уведомлений
schedule_notifications()

# Немедленно отправляем уведомления для проверки
send_notification(reg_day.id, user.id, '1 day')
send_notification(reg_hour.id, user.id, '1 hour')
send_notification(reg_minutes.id, user.id, '5 minutes')
