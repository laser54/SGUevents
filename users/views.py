import os
import json
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from .forms import RegistrationForm
from .telegram_utils import send_login_details_sync
from django.views.decorators.http import require_http_methods

User = get_user_model()

def home(request):
    return render(request, 'users/home.html')

def register(request):
    form = RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.password = get_random_string(8)
        user.set_password(user.password)
        user.save()
        if user.telegram_id:
            send_login_details_sync(user.telegram_id, user.username, user.password)
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form, 'telegram_bot_username': 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'})

def login_view(request):
    context = {'telegram_bot_username': 'Event_dev_sgu_bot' if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, "Вы успешно вошли в систему через логин и пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")
    return render(request, 'users/login.html', context)

@csrf_exempt
@require_http_methods(["POST"])  # Принимать только POST запросы
def telegram_auth(request):
    try:
        data = json.loads(request.body)
        telegram_id = data.get('id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if user:
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'Вы успешно вошли в систему через Telegram.'})
        else:
            return JsonResponse({'success': False, 'error': 'Пользователь не зарегистрирован. Пожалуйста, пройдите регистрацию.', 'redirect_url': '/register'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Некорректные входные данные'})

def general(request):
    return render(request, 'main/index.html')
