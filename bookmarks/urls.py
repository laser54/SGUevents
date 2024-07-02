from django.urls import path
from bookmarks import views

app_name = 'bookmarks'

urlpatterns = [
    path('events_add/', views.events_add, name='events_add'),
    path('events_add/<slug:event_slug>/', views.events_add, name='events_add'),
	path('events_remove/<int:event_id>/', views.events_remove, name='events_remove'),

    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<slug:event_slug>/', views.favorites, name='toggle_favorite'),
	

	path('events_attended/', views.events_attended, name='events_attended'),
	path('events_attended/<slug:event_slug>/', views.events_attended, name='events_attended'),
 
    path('events_registered/', views.events_registered, name='events_registered'),
    path('events_registered/<slug:event_slug>/', views.events_registered, name='events_registered'),
    path('registered_remove/<int:event_id>/', views.registered_remove, name='registered_remove'),
	
    path('registered/', views.registered, name='registered'),
    path('registered/<slug:event_slug>/', views.registered, name='registered'),
    
 

]
