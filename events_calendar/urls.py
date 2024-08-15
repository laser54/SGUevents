from django.urls import path, include
from events_calendar import views

app_name = 'events_calendar'

urlpatterns = [
    path('', views.calendar_view, name='index'),
]