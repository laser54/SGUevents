from django.urls import path, include
from events_cultural import views

app_name = 'events_cultural'

urlpatterns = [
	path('attractions/', views.attractions, name='attractions'),
	path('attractions/<int:page>/', views.attractions, name='attractions'),
	path('attractions/event/<int:event_id>/', views.attractions_card, name='attractions_card'),
	path('attractions/event/<slug:event_slug>/', views.attractions_card, name='attractions_card'),

	path('events_registered/', views.events_registered, name='events_registered'),
	# path('events_registered/<int:event_id>', views.events_registered_, name='events_registered_card'),
	# path('events_registered/event/<slug:event_slug>/', views.events_registered, name='events_registered_card'),

	path('events_for_visiting/', views.events_for_visiting, name='events_for_visiting'),
	path('events_for_visiting/<int:page>/', views.events_for_visiting, name='events_for_visiting'),
	path('events_for_visiting/<int:event_id>', views.for_visiting_card, name='events_for_visiting_card'),
	path('events_for_visiting/event/<slug:event_slug>/', views.for_visiting_card, name='events_for_visiting_card'),
]