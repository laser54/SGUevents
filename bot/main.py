import asyncio
import logging
import os
import sys

import django
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SGUevents.settings")

if 'django' not in sys.modules:
    django.setup()

logging.basicConfig(level=logging.INFO)
TOKEN = settings.ACTIVE_TELEGRAM_BOT_TOKEN

dp = Dispatcher()
User = get_user_model()


async def get_user_profile(telegram_id):
    try:
        return await sync_to_async(User.objects.get)(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None


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
    await message.answer("Вас приветствует Event бот СГУ", reply_markup=keyboard)


@dp.message(F.text == "\U0001F464 Мой профиль")
async def profile(message: types.Message):
    try:
        user = await get_user_profile(message.from_user.id)
        if user:
            department_name = await sync_to_async(get_department_name)(user)
            full_name = f"{user.last_name} {user.first_name}" + (f" {user.middle_name}" if user.middle_name else "")
            response_text = f"Ваше ФИО: {full_name}\nОтдел: {department_name}"
        else:
            response_text = "Вы не зарегистрированы на портале."
    except User.DoesNotExist:
        response_text = "Вы не зарегистрированы на портале."
    except Exception as e:
        response_text = "Произошла ошибка при получении вашего профиля."
        logging.error(f"Error fetching profile: {e}")
    await message.answer(response_text)


def get_department_name(user):
    # Эта функция теперь синхронная
    return user.department.department_name if user.department else "Не указан"


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
