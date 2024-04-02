from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.log_in, name='login'),
    # path('signup/', views.sign_up, name='signup'),
    path('register/', views.register, name='register'),
]
