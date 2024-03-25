from django.urls import path, include
from bookmarks import views

app_name = 'bookmarks'

urlpatterns = [
    path('', views.index, name='index'),
]