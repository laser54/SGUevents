import os

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from .forms import RegistrationForm
from .telegram_utils import send_login_details_sync
User = get_user_model()

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

            # Так как ваша функция send_login_details_sync предполагает синхронный вызов,
            # Не требуется специальной обработки для асинхронности.
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
            auth_login(request, user)
            return redirect('users:home')
        else:
            messages.error(request, "Неверный логин или пароль.")
    return render(request, 'users/login.html')
