from django.shortcuts import render, redirect
from .forms import RegistrationForm
import os


def home(request):
    # Представление для главной страницы
    return render(request, 'users/home.html')


def register(request):
    # Инициализируем форму регистрации
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Если форма валидна, сохраняем нового пользователя
            new_user = form.save(commit=False)
            # Здесь можно добавить дополнительную логику обработки, если это необходимо
            # Например, обработка или сохранение telegram_id из формы
            new_user.save()
            # После успешной регистрации перенаправляем пользователя на главную страницу
            return redirect('users:home')
    else:
        form = RegistrationForm()

    # Определяем имя пользователя Telegram бота в зависимости от окружения
    bot_username = 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'

    # Передаем форму и имя пользователя бота в контекст для рендеринга в шаблоне
    context = {
        'form': form,
        'telegram_bot_username': bot_username,
    }
    return render(request, 'users/register.html', context)
