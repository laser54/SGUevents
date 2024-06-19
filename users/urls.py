from django.urls import path
from .views import home, login_view, register, profile, general, telegram_auth, change_password, request_admin_rights, logout

app_name = 'users'

urlpatterns = [
    # path('', home, name='home'),
    path('', login_view, name='login'),
    path('register/', register, name='register'),
    path('general/', general, name='general'),
    path('telegram-auth/', telegram_auth, name='telegram_auth'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('request-admin-rights/', request_admin_rights, name='request-admin-rights'),
	path('logout/', logout, name="logout"),
]
