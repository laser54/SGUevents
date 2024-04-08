from django.conf import settings

def send_login_details_sync(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"
    settings.TELEGRAM_BOT.send_message(chat_id=telegram_id, text=message_text)
