from django.urls import path
from .views import login_view, register, profile, logout, telegram_auth, change_password, request_admin_rights

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('telegram-auth/', telegram_auth, name='telegram_auth'),
    path('change-password/', change_password, name='change_password'),
    path('request-admin-rights/', request_admin_rights, name='request_admin_rights'),
]
