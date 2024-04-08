from django.urls import path, include
from events_available import views

app_name = 'events_available'

urlpatterns = [
  path('online/', views.online, name='online'),
	path('offline/', views.offline, name='offline'),
	
]