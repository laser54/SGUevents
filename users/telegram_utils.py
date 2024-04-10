import requests
from django.conf import settings


def send_login_details_sync(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"

    # URL для отправки сообщения через Telegram Bot API
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"

    # Параметры запроса
    data = {
        "chat_id": telegram_id,
        "text": message_text,
    }

    # Выполнение POST-запроса
    response = requests.post(send_url, data=data)

    # Проверка успешности запроса
    if not response.ok:
        print(f"Ошибка отправки сообщения: {response.text}")
