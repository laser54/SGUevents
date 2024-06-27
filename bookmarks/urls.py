from django.urls import path
from bookmarks import views

app_name = 'bookmarks'

urlpatterns = [
    path('events_add/', views.events_add, name='events_add'),
    path('events_add/<slug:event_slug>/', views.events_add, name='events_add'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<slug:event_slug>/', views.favorites, name='toggle_favorite'),
	path('events_attended/', views.events_attended, name='events_attended'),
	path('events_attended/<slug:event_slug>/', views.events_attended, name='events_attended')

]
