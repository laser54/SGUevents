import asyncio
import logging

import requests
import json
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.contrib.contenttypes.models import ContentType

load_dotenv()
from bot.django_initializer import setup_django_environment

from django.contrib.auth import get_user_model
from django.conf import settings
logging.basicConfig(level=logging.INFO)

# Initialize bot
TOKEN = settings.ACTIVE_TELEGRAM_BOT_TOKEN
SUPPORT_CHAT_ID = settings.ACTIVE_TELEGRAM_SUPPORT_CHAT_ID
storage = MemoryStorage()
dp = Dispatcher()
router = Router()

class SupportRequestForm(StatesGroup):
    waiting_for_question = State()

class ReviewForm(StatesGroup):
    waiting_for_review = State()


async def get_user_profile(telegram_id):
    User = get_user_model()
    try:
        return await sync_to_async(User.objects.get)(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None

async def get_user_events(user):
    from bookmarks.models import Registered
    events = await sync_to_async(list)(Registered.objects.filter(user=user))
    event_details = []
    for event in events:
        if await sync_to_async(lambda: event.online)():
            event_name = await sync_to_async(lambda: event.online.name)()
        elif await sync_to_async(lambda: event.offline)():
            event_name = await sync_to_async(lambda: event.offline.name)()
        elif await sync_to_async(lambda: event.attractions)():
            event_name = await sync_to_async(lambda: event.attractions.name)()
        elif await sync_to_async(lambda: event.for_visiting)():
            event_name = await sync_to_async(lambda: event.for_visiting.name)()
        else:
            event_name = "Неизвестное мероприятие"
        event_details.append(event_name)
    return event_details


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
async def my_events(message: types.Message):
    user = await get_user_profile(message.from_user.id)
    if user:
        event_details = await get_user_events(user)
        if event_details:
            for event_name in event_details:
                response_text = f"Мероприятие: {event_name}"
                await message.answer(response_text)
        else:
            await message.answer("Вы не зарегистрированы на какие-либо мероприятия.")
    else:
        await message.answer("Вы не зарегистрированы на портале.")


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
    from users.models import SupportRequest
    user = await get_user_profile(message.from_user.id)
    if user:
        # Сохраняем вопрос в базе данных
        support_request = await sync_to_async(SupportRequest.objects.create)(
            user=user,
            question=message.text
        )
        # Отправляем вопрос в чат поддержки
        support_message = f"Новый вопрос от пользователя {user.username}:\n\n{message.text}"
        send_message_to_support_chat(support_message)
        await message.answer("Ваш вопрос отправлен в техподдержку. Спасибо!")
    else:
        await message.answer("Вы не зарегистрированы на портале.")
    await state.clear()
def send_message_to_support_chat(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': SUPPORT_CHAT_ID,
        'text': text
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}, {response.text}")


@router.callback_query(F.data.startswith("toggle_"))
async def toggle_notification(callback_query: types.CallbackQuery):
    event_id = callback_query.data.split("_")[1]
    user = await get_user_profile(callback_query.from_user.id)
    if user:
        from bookmarks.models import Registered
        registration = await sync_to_async(Registered.objects.get)(user=user, id=event_id)
        registration.notifications_enabled = not registration.notifications_enabled
        await sync_to_async(registration.save)()

        new_button_text = "\U0001F7E2 Включить уведомления" if not registration.notifications_enabled else "\U0001F534 Отключить уведомления"
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=new_button_text, callback_data=f"toggle_{event_id}")]
        ])
        await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard)
        await callback_query.answer(f"Уведомления {'включены' if registration.notifications_enabled else 'отключены'}.")
    else:
        await callback_query.answer("Вы не зарегистрированы на портале.")

@router.callback_query(F.data.startswith("leave_review_"))
async def leave_review(callback_query: types.CallbackQuery, state: FSMContext):
    event_id = callback_query.data.split("_")[2]
    user = await get_user_profile(callback_query.from_user.id)
    if user:
        await callback_query.message.answer("Пожалуйста, напишите ваш отзыв:")
        await state.set_state(ReviewForm.waiting_for_review)
        await state.update_data(event_id=event_id)
    else:
        await callback_query.answer("Вы не зарегистрированы на портале.")

@router.callback_query(F.data.startswith("review_later_"))
async def remind_later(callback_query: types.CallbackQuery):
    await callback_query.answer("Хорошо, напомним позже.")
    # Логика для напоминания позже может быть добавлена здесь

@router.message(ReviewForm.waiting_for_review)
async def receive_review(message: types.Message, state: FSMContext):
    user = await get_user_profile(message.from_user.id)
    data = await state.get_data()
    event_id = data.get("event_id")
    if user and event_id:
        from bookmarks.models import Registered
        from events_cultural.models import Review
        content_type = await sync_to_async(ContentType.objects.get_for_model)(Registered)
        review = await sync_to_async(Review.objects.create)(
            user=user,
            content_type=content_type,
            object_id=event_id,
            comment=message.text
        )
        await message.answer("Спасибо за ваш отзыв!")
        await state.clear()
    else:
        await message.answer("Произошла ошибка, попробуйте снова.")
        await state.clear()

# Функция запуска бота
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
async def run_bot():
    try:
        dp.include_router(router)
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == "__main__":
    setup_django_environment()
    asyncio.run(run_bot())
