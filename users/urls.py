from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),
    path('signup/', views.sign_up, name='signup'),
    # Добавляем новый путь для обработки формы регистрации
    path('register/', views.register, name='register'),
]
