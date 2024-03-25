from django.urls import path, include
from events_cultural import views

app_name = 'events_cultural'

urlpatterns = [
    path('', views.index, name='index'),
]