from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from bookmarks.models import Favorite, Registered
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting

@login_required
def events_add(request, event_slug):
    try:
        event = Events_online.objects.get(slug=event_slug)
        event_type = 'online'
    except Events_online.DoesNotExist:
        try:
            event = Events_offline.objects.get(slug=event_slug)
            event_type = 'offline'
        except Events_offline.DoesNotExist:
            try:
                event = Attractions.objects.get(slug=event_slug)
                event_type = 'attractions'
            except Attractions.DoesNotExist:
                try:
                    event = Events_for_visiting.objects.get(slug=event_slug)
                    event_type = 'for_visiting'
                except Events_for_visiting.DoesNotExist:
                    event = None
                    event_type = None

    if event and request.user.is_authenticated:
        if event_type == 'online':
            Favorite.objects.get_or_create(user=request.user, online=event)
        elif event_type == 'offline':
            Favorite.objects.get_or_create(user=request.user, offline=event)
        elif event_type == 'attractions':
            Favorite.objects.get_or_create(user=request.user, attractions=event)
        elif event_type == 'for_visiting':
            Favorite.objects.get_or_create(user=request.user, for_visiting=event)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def events_remove(request, event_id):

    event = Favorite.objects.get(id=event_id)
    event.delete()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {'favorites': favorites}
    return render(request, 'bookmarks/favorites.html', context)

def events_attended(request):
    pass
    return render(request, "bookmarks/events_attended.html")

@login_required
def events_registered(request, event_slug):
    try:
        event = Events_online.objects.get(slug=event_slug)
        event_type = 'online'
    except Events_online.DoesNotExist:
        try:
            event = Events_offline.objects.get(slug=event_slug)
            event_type = 'offline'
        except Events_offline.DoesNotExist:
            try:
                event = Attractions.objects.get(slug=event_slug)
                event_type = 'attractions'
            except Attractions.DoesNotExist:
                try:
                    event = Events_for_visiting.objects.get(slug=event_slug)
                    event_type = 'for_visiting'
                except Events_for_visiting.DoesNotExist:
                    event = None
                    event_type = None

    if event and request.user.is_authenticated:
        if event_type == 'online':
            Registered.objects.get_or_create(user=request.user, online=event)
        elif event_type == 'offline':
            Registered.objects.get_or_create(user=request.user, offline=event)
        elif event_type == 'attractions':
            Registered.objects.get_or_create(user=request.user, attractions=event)
        elif event_type == 'for_visiting':
            Registered.objects.get_or_create(user=request.user, for_visiting=event)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def registered(request):
    registered = Registered.objects.filter(user=request.user)
    context = {'favorites': registered}
    return render(request, 'bookmarks/registered.html', context)