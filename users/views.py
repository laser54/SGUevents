import os
import json
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Функция для определения данных виджета Telegram
def get_telegram_widget_data():
    django_env = os.getenv('DJANGO_ENV', 'development')
    if django_env == 'production':
        # Данные для продакшен виджета
        return {
            'script_src': "https://telegram.org/js/telegram-widget.js?7&production=1",
            'bot_username': 'event_sgu_bot',  # Измените на имя вашего бота для продакшена
            'data_size': 'large'
        }
    else:
        # Данные для виджета в разработке
        return {
            'script_src': "https://telegram.org/js/telegram-widget.js?7&development=1",
            'bot_username': 'Event_dev_sgu_bot',  # Измените на имя вашего бота для разработки
            'data_size': 'small'
        }

def index(request):
    # Добавляем данные виджета в контекст шаблона
    telegram_data = get_telegram_widget_data()
    context = {'telegram_data': telegram_data}
    return render(request, 'users/index.html', context)

def log_in(request):
    return render(request, 'users/users_log_in.html')

def sign_up(request):
    # Также добавляем данные виджета в контекст для страницы регистрации
    telegram_data = get_telegram_widget_data()
    context = {'telegram_data': telegram_data}
    return render(request, 'users/users_sign_up.html', context)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        telegram_data_raw = request.POST.get('telegramData')
        if telegram_data_raw:
            telegram_data = json.loads(telegram_data_raw)

            # Проверка, существует ли уже пользователь с таким Telegram ID
            if Profile.objects.filter(telegram_id=telegram_data['id']).exists():
                return HttpResponse('Пользователь с таким Telegram ID уже существует.', status=400)

            # Создание нового пользователя
            user = User.objects.create_user(username=telegram_data.get('username'), password='УникальныйПароль')

            # Создание профиля пользователя с Telegram ID
            Profile.objects.create(user=user, telegram_id=telegram_data['id'])

            return HttpResponse('Регистрация успешно завершена.')
        else:
            return HttpResponse('Ошибка: отсутствуют данные Telegram.', status=400)
    else:
        return HttpResponse('Метод не поддерживается.', status=405)
