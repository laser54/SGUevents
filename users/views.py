import os
import json
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .telegram_utils import send_login_details_sync
from .models import Department  # Импорт модели отдела

User = get_user_model()
logger = logging.getLogger(__name__)

DEV_BOT_NAME = os.getenv('DEV_BOT_NAME')

def home(request):
    return render(request, 'users/home.html')

def success(request):
    login_method = request.session.get('login_method', 'Неизвестный способ входа')
    return render(request, 'users/success.html', {'login_method': login_method})

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            generated_password = get_random_string(8)
            department_id = form.cleaned_data['department_id']
            department, _ = Department.objects.get_or_create(department_id=department_id)

            user_kwargs = {
                'email': form.cleaned_data.get('email'),
                'password': generated_password,
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'middle_name': form.cleaned_data.get('middle_name', ''),
                'department': department,
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
        'telegram_bot_username': DEV_BOT_NAME if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot',
    }
    return render(request, 'users/register.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            request.session['login_method'] = 'Через логин и пароль'
            return redirect('users:success')
        else:
            messages.error(request, "Неверный логин или пароль.")
    context = {
        'telegram_bot_username': DEV_BOT_NAME if os.getenv('DJANGO_ENV') == 'development' else 'Event_sgu_bot'
    }
    return render(request, 'users/login.html', context)

@csrf_exempt
def telegram_auth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        telegram_id = data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if user:
            auth_login(request, user)
            request.session['login_method'] = 'Через Telegram'
            return JsonResponse({'success': True, 'redirect_url': '/success'})
        else:
            return JsonResponse({'success': False, 'error': 'User not registered. Please register.', 'redirect_url': '/register'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
@login_required
def change_password(request):
    if request.method == 'POST' and request.user.telegram_id:
        new_password = get_random_string(8)
        request.user.set_password(new_password)
        request.user.save()
        send_login_details_sync(request.user.telegram_id, request.user.username, new_password)
        return JsonResponse({'success': True, 'message': 'Your password has been successfully changed and sent via Telegram.'})
    return JsonResponse({'success': False, 'error': 'Access denied.'})

def general(request):
    return render(request, 'main/index.html')
