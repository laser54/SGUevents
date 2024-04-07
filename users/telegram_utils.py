import asyncio
from django.conf import settings

async def send_login_password(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"
    await settings.TELEGRAM_BOT.send_message(chat_id=telegram_id, text=message_text)


def send_login_details_sync(telegram_id, login, password):
    asyncio.run(send_login_password(telegram_id, login, password))
