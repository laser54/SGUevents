from django.urls import path
from .views import home, login_view, register, general, telegram_auth, success, change_password, request_admin_rights

app_name = 'users'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('general/', general, name='general'),
    path('telegram-auth/', telegram_auth, name='telegram_auth'),
    path('success/', success, name='success'),
    path('change-password/', change_password, name='change_password'),
    path('request-admin-rights/', request_admin_rights, name='request-admin-rights'),
]
