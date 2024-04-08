from django.urls import path, include
from events_cultural import views

app_name = 'events_cultural'

urlpatterns = [
  path('attractions/', views.attractions, name='attractions'),
	path('events_registered/', views.events_registered, name='events_registered'),
	path('events_for_visiting/', views.events_for_visiting, name='events_for_visiting'),
]