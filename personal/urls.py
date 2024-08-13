from django.urls import include, path
from . import views

app_name = 'personal'

urlpatterns = [
    path('', views.personal, name='personal'),
    path('add_online_event/', views.add_online_event, name='add_online_event'),
    path('add_offline_event/', views.add_offline_event, name='add_offline_event'),
	path('select2/', include('django_select2.urls')),
]
