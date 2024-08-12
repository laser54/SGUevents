import uuid

import requests
import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from aiogram.utils.keyboard import InlineKeyboardBuilder




logger = logging.getLogger('my_debug_logger')


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


def send_message_to_user(telegram_id, message, event_id=None, reply_markup=None):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message,
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    response = requests.post(send_url, data=data)
    if response.ok:
        print(f"Сообщение успешно отправлено пользователю с telegram_id: {telegram_id}")
    else:
        print(f"Ошибка отправки сообщения пользователю: {response.text}")

def send_message_to_user_with_toggle_button(telegram_id, message, event_id, notifications_enabled):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    button_text = "\U0001F534 Отключить уведомления" if notifications_enabled else "\U0001F7E2 Включить уведомления"
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

def send_message_to_user(telegram_id, message, event_id=None, reply_markup=None):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message,
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    response = requests.post(send_url, data=data)
    if response.ok:
        print(f"Сообщение успешно отправлено пользователю с telegram_id: {telegram_id}")
    else:
        print(f"Ошибка отправки сообщения пользователю: {response.text}")

def send_message_to_user_with_toggle_button(telegram_id, message, event_id, notifications_enabled):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    button_text = "\U0001F534 Отключить уведомления" if notifications_enabled else "\U0001F7E2 Включить уведомления"
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



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


logger = logging.getLogger('my_debug_logger')

def inline_keyboard_to_dict(inline_keyboard):
    """
    Преобразует объект InlineKeyboardMarkup в словарь.
    """
    keyboard = []
    for row in inline_keyboard.inline_keyboard:
        row_buttons = []
        for button in row:
            button_data = {
                "text": button.text,
                "callback_data": button.callback_data
            }
            row_buttons.append(button_data)
        keyboard.append(row_buttons)
    return {"inline_keyboard": keyboard}

def send_message_to_user_with_review_buttons(telegram_id, message, event_id, event_type):
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"

    # Проверяем, что event_id является валидным UUID
    try:
        uuid_obj = uuid.UUID(event_id)  # Проверка UUID
    except ValueError:
        print(f"Некорректный UUID: {event_id}")
        return

    # Создаем клавиатуру
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="\U0000270D Оставить отзыв",
                callback_data=f"review:{uuid_obj}:{event_type}"
            )
        ]
    ])

    data = {
        "chat_id": telegram_id,
        "text": message,
        "reply_markup": inline_keyboard_to_dict(reply_markup)
    }

    response = requests.post(send_url, json=data)
    if response.ok:
        print(f"Сообщение успешно отправлено пользователю с telegram_id: {telegram_id}")
    else:
        print(f"Ошибка отправки сообщения пользователю: {response.text}")
