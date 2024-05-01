from django.urls import path, include
from events_available import views

app_name = 'events_available'

urlpatterns = [
	path('online/', views.online, name='online'),
	path('online/<int:page>/', views.online, name='online'),
    
	path('online/event/<int:event_id>/', views.online_card, name='online_card'),
	path('online/event/<slug:event_slug>/', views.online_card, name='online_card'),

	path('offline/', views.offline, name='offline'),
	path('offline/<int:page>/', views.offline, name='offline'),
	path('offline/event/<int:event_id>/', views.offline_card, name='offline_card'),
	path('offline/event/<slug:event_slug>/', views.offline_card, name='offline_card'),
]