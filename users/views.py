from django.contrib.auth.models import User
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def index(request):
    return render(request, 'users/index.html')

def log_in(request):
    return render(request, 'users/users_log_in.html')

def sign_up(request):
    return render(request, 'users/users_sign_up.html')
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
