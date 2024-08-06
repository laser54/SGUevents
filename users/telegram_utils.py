import requests
import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ADMIN_TG_NAME = os.getenv("ADMIN_TG_NAME")

def send_login_details_sync(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message_text,
    }
    response = requests.post(send_url, data=data)
    if not response.ok:
        print(f"Ошибка отправки сообщения: {response.text}")

def send_message_to_admin(telegram_id, message):
    admin_tg_username = ADMIN_TG_NAME
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"



    data = {
        "chat_id": admin_tg_username,
        "text": message,
            }

    print("Sending message to admin:", admin_tg_username)
    response = requests.post(send_url, data=data)
    if not response.ok:
        print(f"Ошибка отправки сообщения администратору: {response.text}")

def send_confirmation_to_user(telegram_id):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    confirmation_message = "Ваш запрос на предоставление админских прав был отправлен администратору."
    data = {
        "chat_id": telegram_id,
        "text": confirmation_message,
    }
    response = requests.post(send_url, data=data)
    if not response.ok:
        print(f"Ошибка отправки подтверждающего сообщения пользователю: {response.text}")


def send_message_to_user(telegram_id, message):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message,
    }
    response = requests.post(send_url, data=data)
    if response.ok:
        print(f"Сообщение успешно отправлено пользователю с telegram_id: {telegram_id}")
    else:
        print(f"Ошибка отправки сообщения пользователю: {response.text}")

def send_message_to_user_with_toggle_button(telegram_id, message, event_id, notifications_enabled):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    button_text = "Отключить уведомления" if notifications_enabled else "Включить уведомления"
    callback_data = f"toggle_{event_id}"
    inline_keyboard = {
        "inline_keyboard": [[
            {
                "text": button_text,
                "callback_data": callback_data
            }
        ]]
    }
    data = {
        "chat_id": telegram_id,
        "text": message,
        "reply_markup": json.dumps(inline_keyboard)
    }
    response = requests.post(send_url, data=data)
    if response.ok:
        print(f"Сообщение успешно отправлено пользователю с telegram_id: {telegram_id}")
    else:
        print(f"Ошибка отправки сообщения пользователю: {response.text}")
