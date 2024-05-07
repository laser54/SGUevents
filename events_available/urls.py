from django.urls import path, include
from events_available import views

app_name = 'events_available'

urlpatterns = [
	path('online/<int:page>/', views.online, name='online'),
	path('online/', views.online, name='online'),
    
	# path('online/<int:event_id>/', views.online_card, name='online_card'),
	path('online/<slug:event_slug>/', views.online_card, name='online_card'),

	path('offline/', views.offline, name='offline'),
	# path('offline/<int:page>/', views.offline, name='offline'),
	# path('offline/<int:event_id>/', views.offline_card, name='offline_card'),
	path('offline/<slug:event_slug>/', views.offline_card, name='offline_card'),
]