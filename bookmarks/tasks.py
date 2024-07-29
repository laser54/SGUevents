# bookmarks/tasks.py
from celery import shared_task
from users.telegram_utils import send_message_to_admin

@shared_task
def send_test_message():
    send_message_to_admin("1349308", "Это тестовое сообщение от Celery.")
