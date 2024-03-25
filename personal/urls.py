from django.urls import path, include
from personal import views

app_name = 'personal'

urlpatterns = [
    path('', views.index, name='index'),
]