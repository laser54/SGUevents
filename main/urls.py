from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
		path('support/', include('support.urls', namespace='support')),
		path('events_available/', include('events_available.urls', namespace='events_available'))
]