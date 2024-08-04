from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting
import json

@login_required
def calendar_view(request):
    events_online = Events_online.objects.all()
    events_offline = Events_offline.objects.all()
    attractions = Attractions.objects.all()
    events_for_visiting = Events_for_visiting.objects.all()
    
    events = []
    for event in events_online:
        events.append({
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Онлайн'
        })

    for event in events_offline:
        events.append({
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Оффлайн'
        })

    for event in attractions:
        events.append({
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Достопримечательность'
        })

    for event in events_for_visiting:
        events.append({
            'title': f"{event.name}",
            'start': event.date.strftime("%Y-%m-%d"),
            'time': event.time_start.strftime("%H:%M"),
            'category': 'Для посещения'
        })

    context = {
        'events': json.dumps(events)
    }
    return render(request, 'events_calendar/index.html', context)
