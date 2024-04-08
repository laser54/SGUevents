from django.urls import path
from . import views
from .views import login_view

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    # path('signup/', views.sign_up, name='signup'),
    path('register/', views.register, name='register'),
]
