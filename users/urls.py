from django.urls import path
from . import views
from .views import login_view, register, home, general, telegram_auth

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('general/', views.general, name='general'),
    path('register/', views.register, name='register'),
    path('telegram-auth/', telegram_auth, name='telegram_auth'),
]
