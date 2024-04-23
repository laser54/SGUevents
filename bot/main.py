import asyncio
import django
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from django.conf import settings


load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")
django.setup()

TOKEN = settings.ACTIVE_TELEGRAM_BOT_TOKEN

# Инициализация бота и диспетчера
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="\U0001F464 Мой профиль"),
            types.KeyboardButton(text="\U0001F5D3 Мои мероприятия"),
            types.KeyboardButton(text="\U00002754 Помощь")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню"
    )
    await message.answer("Вас приветсвует Event бот СГУ", reply_markup=keyboard)

@dp.message(F.text == "\U0001F464 Мой профиль")
async def with_puree(message: types.Message):
    await message.answer("Функция 'Профиль' еще не реализована. Подождите немного!")

@dp.message(F.text == "\U0001F5D3 Мои мероприятия")
async def without_puree(message: types.Message):
    await message.answer("Функция 'Мои мероприятия' еще не реализована. Подождите немного!")

@dp.message(F.text == "\U00002754 Помощь")
async def without_puree(message: types.Message):
    await message.answer("Функция 'Помощь' еще не реализована. Подождите немного!")

# Функция запуска бота
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
async def run_bot():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
