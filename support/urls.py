from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from support import views

app_name = 'support'

urlpatterns = [
    path('', views.index, name='index'),
]