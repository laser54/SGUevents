import requests
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def send_login_details_sync(telegram_id, login, password):
    message_text = f"Ваши учетные данные для входа:\nЛогин: {login}\nПароль: {password}"
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message_text,
    }
    response = requests.post(send_url, data=data)
    if not response.ok:
        print(f"Ошибка отправки сообщения: {response.text}")

def send_message_to_admin(telegram_id, message):
    # admin_tg_username = '@la5er'
    admin_tg_username = settings.ADMIN_TG_NAME  # Assuming the admin's username includes '@'
    send_url = f"https://api.telegram.org/bot{settings.ACTIVE_TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": admin_tg_username,
        "text": message,
    }
    response = requests.post(send_url, data=data)
    if not response.ok:
        print(f"Ошибка отправки сообщения администратору: {response.text}")

@csrf_exempt
@login_required
def request_admin_rights(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            justification = data.get('reason', '')
            user_full_name = f"{request.user.last_name} {request.user.first_name} {' ' + request.user.middle_name if request.user.middle_name else ''}".strip()
            message = f"Запрос на админские права от {user_full_name}: {justification}"
            send_message_to_admin(request.user.telegram_id, message)
            return JsonResponse({'success': True, 'message': 'Запрос на админские права отправлен администратору.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Ошибка в формате данных.'})
    return JsonResponse({'success': False, 'error': 'Недопустимый запрос.'})
