from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from .telegram_utils import send_login_details_sync
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
import os

User = get_user_model()  # Получаем модель пользователя


def home(request):
    # Представление для главной страницы
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Генерируем пароль перед созданием пользователя
            generated_password = get_random_string(8)

            # Создаем пользователя
            user_kwargs = {
                'email': form.cleaned_data.get('email'),  # Может быть None
                'password': generated_password,  # Используем заранее сгенерированный пароль
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'middle_name': form.cleaned_data.get('middle_name', ''),
                'department_id': form.cleaned_data['department_id'],
                'telegram_id': form.cleaned_data['telegram_id'],
            }
            new_user = User.objects.create_user(**user_kwargs)

            # Отправляем логин и пароль через Telegram
            if new_user.telegram_id:
                send_login_details_sync(new_user.telegram_id, new_user.username, generated_password)

            return redirect('users:login')
    else:
        form = RegistrationForm()

    bot_username = 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'

    context = {
        'form': form,
        'telegram_bot_username': bot_username,
    }
    return render(request, 'users/register.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:home')  # Перенаправляем на главную страницу после логина
        else:
            messages.error(request, "Неверный логин или пароль.")
    return render(request, 'users/login.html')
