from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.log_in, name='users_log_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
]