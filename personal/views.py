from itertools import chain
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting

# @login_required
# def add_online_event(request):
#     if request.method == 'POST':
#         form = EventsOnlineForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('personal:personal'))
#     else:
#         form = EventsOnlineForm()

#     form_html = render_to_string('personal/event_form.html', {'form': form})
#     return JsonResponse({'form_html': form_html})

# @login_required
# def add_offline_event(request):
#     if request.method == 'POST':
#         form = EventsOfflineForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('personal:personal'))
#     else:
#         form = EventsOfflineForm()

#     form_html = render_to_string('personal/event_form.html', {'form': form})
#     return JsonResponse({'form_html': form_html})

@login_required
def personal(request):
    current_user = request.user
    if current_user.is_staff:
        online_events = Events_online.objects.filter(events_admin=current_user.username)
        offline_events = Events_offline.objects.filter(events_admin=current_user.username)
        attractions = Attractions.objects.filter(events_admin=current_user.username)
        for_visiting = Events_for_visiting.objects.filter(events_admin=current_user.username)
    else:
        online_events = []
        offline_events = []
        attractions = []
        for_visiting = []

    
    events = list(chain(online_events, offline_events, attractions, for_visiting))

    context = {
        'event_card_views': events,
        'online_events': online_events,
        'offline_events': offline_events,
    }
    
    return render(request, 'personal/personal.html', context)
