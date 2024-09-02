from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting
from bookmarks.models import Registered, Favorite
from django.urls import reverse
import json

@login_required
def calendar_view(request):
    events_online = Events_online.objects.all()
    events_offline = Events_offline.objects.all()
    attractions = Attractions.objects.all()
    events_for_visiting = Events_for_visiting.objects.all()
    
    registered_online_ids = Registered.objects.filter(user=request.user, online__isnull=False).values_list('online_id', flat=True)
    registered_offline_ids = Registered.objects.filter(user=request.user, offline__isnull=False).values_list('offline_id', flat=True)
    registered_attractions_ids = Registered.objects.filter(user=request.user, attractions__isnull=False).values_list('attractions_id', flat=True)
    registered_for_visiting_ids = Registered.objects.filter(user=request.user, for_visiting__isnull=False).values_list('for_visiting_id', flat=True)

    favorite_online_ids = Favorite.objects.filter(user=request.user, online__isnull=False).values_list('online_id', flat=True)
    favorite_offline_ids = Favorite.objects.filter(user=request.user, offline__isnull=False).values_list('offline_id', flat=True)
    favorite_attractions_ids = Favorite.objects.filter(user=request.user, attractions__isnull=False).values_list('attractions_id', flat=True)
    favorite_for_visiting_ids = Favorite.objects.filter(user=request.user, for_visiting__isnull=False).values_list('for_visiting_id', flat=True)
    
    events = []
    for event in events_online:
        event_data = {
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Онлайн',
            'backgroundColor': 'rgb(30, 141, 30)',  # Зеленый цвет по умолчанию
            'url': reverse('events_available:online_card', args=[event.slug])
        }
        if event.id in registered_online_ids:
            event_data['backgroundColor'] = 'yellow'  # Желтый цвет для зарегистрированных мероприятий
        elif event.id in favorite_online_ids:
            event_data['backgroundColor'] = 'pink'  # Розовый цвет для избранных мероприятий
        events.append(event_data)

    for event in events_offline:
        event_data = {
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Оффлайн',
            'backgroundColor': 'rgb(30, 141, 30)',  # Зеленый цвет по умолчанию
            'url': reverse('events_available:offline_card', args=[event.slug])
        }
        if event.id in registered_offline_ids:
            event_data['backgroundColor'] = 'yellow'  # Желтый цвет для зарегистрированных мероприятий
        elif event.id in favorite_offline_ids:
            event_data['backgroundColor'] = 'pink'  # Розовый цвет для избранных мероприятий
        events.append(event_data)

    for event in attractions:
        event_data = {
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Достопримечательность',
            'backgroundColor': 'rgb(30, 141, 30)',  # Зеленый цвет по умолчанию
            'url': reverse('events_cultural:attractions_card', args=[event.slug])
        }
        if event.id in registered_attractions_ids:
            event_data['backgroundColor'] = 'yellow'  # Желтый цвет для зарегистрированных мероприятий
        elif event.id in favorite_attractions_ids:
            event_data['backgroundColor'] = 'pink'  # Розовый цвет для избранных мероприятий
        events.append(event_data)

    for event in events_for_visiting:
        event_data = {
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Для посещения',
            'backgroundColor': 'rgb(30, 141, 30)',  # Зеленый цвет по умолчанию
            'url': reverse('events_cultural:events_for_visiting_card', args=[event.slug])
        }
        if event.id in registered_for_visiting_ids:
            event_data['backgroundColor'] = 'yellow'  # Желтый цвет для зарегистрированных мероприятий
        elif event.id in favorite_for_visiting_ids:
            event_data['backgroundColor'] = 'pink'  # Розовый цвет для избранных мероприятий
        events.append(event_data)

    context = {
        'events': json.dumps(events)
    }
    return render(request, 'events_calendar/index.html', context)
