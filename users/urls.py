from django.urls import path
from .views import home, login_view, register, general, telegram_auth, success

app_name = 'users'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('general/', general, name='general'),
    path('telegram-auth/', telegram_auth, name='telegram_auth'),
    path('success/', success, name='success'),
]
