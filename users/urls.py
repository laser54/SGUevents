from django.urls import path
from . import views
from .views import login_view

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('general/', views.general, name='general'),
    path('register/', views.register, name='register'),
]
