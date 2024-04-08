from django.conf import settings
import asyncio

async def send_login_details(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"
    await settings.TELEGRAM_BOT.send_message(chat_id=telegram_id, text=message_text)
