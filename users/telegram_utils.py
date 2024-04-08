from django.conf import settings
import asyncio
from threading import Thread

# Асинхронная функция для отправки сообщения
async def send_login_details_async(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"
    await settings.TELEGRAM_BOT.send_message(chat_id=telegram_id, text=message_text)

# Функция-обертка для синхронного вызова
def send_login_details_sync(telegram_id, login, password):
    # Запуск асинхронной функции в отдельном потоке
    loop = asyncio.new_event_loop()
    t = Thread(target=lambda: loop.run_until_complete(send_login_details_async(telegram_id, login, password)))
    t.start()
    t.join()  # Дожидаемся завершения потока
