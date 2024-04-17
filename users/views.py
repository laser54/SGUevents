import os
import json
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login

from .forms import RegistrationForm
from .telegram_utils import send_login_details_sync

User = get_user_model()
logger = logging.getLogger(__name__)

def home(request):
    # Представление для главной страницы
    return render(request, 'users/home.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            generated_password = get_random_string(8)
            user_kwargs = {
                'email': form.cleaned_data.get('email'),
                'password': generated_password,
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'middle_name': form.cleaned_data.get('middle_name', ''),
                'department_id': form.cleaned_data['department_id'],
                'telegram_id': form.cleaned_data['telegram_id'],
            }
            new_user = User.objects.create_user(**user_kwargs)

            if new_user.telegram_id:
                send_login_details_sync(new_user.telegram_id, new_user.username, generated_password)

            return redirect('users:login')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'telegram_bot_username': 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot',
    }
    return render(request, 'users/register.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('users:home')
        else:
            messages.error(request, "Неверный логин или пароль.")

    telegram_bot_username = 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'

    context = {
        'telegram_bot_username': telegram_bot_username
    }
    return render(request, 'users/login.html', context)

@csrf_exempt
def telegram_auth(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            user = User.objects.filter(telegram_id=telegram_id).first()
            if user:
                auth_login(request, user)
                return JsonResponse({'success': True, 'message': 'Вы успешно вошли в систему через Telegram.'})
            else:
                return JsonResponse({'success': False, 'error': 'Пользователь не зарегистрирован. Пожалуйста, пройдите регистрацию.', 'redirect_url': '/register'})
        except Exception as e:
            logger.error(f"Ошибка при аутентификации через Telegram: {e}")
            return JsonResponse({'success': False, 'error': 'Внутренняя ошибка сервера'})
    return JsonResponse({'success': False, 'error': 'Неверный запрос'})



def general(request):
    # Представление для страницы с контентом
    return render(request, 'main/index.html')
