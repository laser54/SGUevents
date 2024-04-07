from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
import os

User = get_user_model()  # Получаем модель пользователя


def home(request):
    # Представление для главной страницы
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем пользователя с помощью create_user
            user_kwargs = {
                'password': None,  # Пароль будет сгенерирован автоматически, если не указан
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'middle_name': form.cleaned_data.get('middle_name', ''),
                'department_id': form.cleaned_data['department_id'],
                'telegram_id': form.cleaned_data['telegram_id'],
            }
            # Добавляем email, только если он был предоставлен
            if form.cleaned_data.get('email'):
                user_kwargs['email'] = form.cleaned_data['email']

            new_user = User.objects.create_user(**user_kwargs)
            # После успешной регистрации перенаправляем пользователя на главную страницу
            return redirect('users:home')
    else:
        form = RegistrationForm()

    # Определяем имя пользователя Telegram бота в зависимости от окружения
    bot_username = 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'

    context = {
        'form': form,
        'telegram_bot_username': bot_username,
    }
    return render(request, 'users/register.html', context)
