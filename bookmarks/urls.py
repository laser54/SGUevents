from django.urls import path, include
from bookmarks import views

app_name = 'bookmarks'

urlpatterns = [
    path('events_attended/', views.events_attended, name='events_attended'),
    path('events_attended/<slug:event_slug>/', views.events_attended, name='events_attended'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/<slug:event_slug>/', views.favorites, name='favorites'),
]