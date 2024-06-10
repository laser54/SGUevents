import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage


load_dotenv()
from bot.django_initializer import setup_django_environment

from django.contrib.auth import get_user_model
from django.conf import settings
from users.models import SupportRequest
logging.basicConfig(level=logging.INFO)

# Initialize bot
TOKEN = settings.ACTIVE_TELEGRAM_BOT_TOKEN
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class SupportRequestForm(StatesGroup):
    waiting_for_question = State()


async def get_user_profile(telegram_id):
    User = get_user_model()
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
    user = await get_user_profile(message.from_user.id)
    if user:
        department_name = await sync_to_async(get_department_name)(user)
        full_name = f"{user.last_name} {user.first_name}" + (f" {user.middle_name}" if user.middle_name else "")
        response_text = f"Ваше ФИО: {full_name}\nОтдел: {department_name}"
    else:
        response_text = "Вы не зарегистрированы на портале."
    await message.answer(response_text)

def get_department_name(user):
    return user.department.department_name if user.department else "Не указан"

@dp.message(F.text == "\U0001F5D3 Мои мероприятия")
async def without_puree(message: types.Message):
    await message.answer("Функция 'Мои мероприятия' еще не реализована. Подождите немного!")

@dp.message(F.text == "\U00002754 Помощь")
async def help_request(message: types.Message, state: FSMContext):
    user = await get_user_profile(message.from_user.id)
    if user:
        await message.answer("Пожалуйста, введите ваш вопрос:")
        await state.set_state(SupportRequestForm.waiting_for_question)
    else:
        await message.answer("Вы не зарегистрированы на портале.")

@dp.message(SupportRequestForm.waiting_for_question)
async def receive_question(message: types.Message, state: FSMContext):
    user = await get_user_profile(message.from_user.id)
    if user:
        # Сохраняем вопрос в базе данных
        support_request = await sync_to_async(SupportRequest.objects.create)(
            user=user,
            question=message.text
        )
        await message.answer("Ваш вопрос отправлен в техподдержку. Спасибо!")
    else:
        await message.answer("Вы не зарегистрированы на портале.")
    await state.clear()

# Функция запуска бота
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def run_bot():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == "__main__":
    setup_django_environment()
    asyncio.run(run_bot())
