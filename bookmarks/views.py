from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from bookmarks.models import Favorite, Registered
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting


@login_required
def events_add(request, event_slug):
    event = None
    event_type = None
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
                    pass

    if event and request.user.is_authenticated:
        favorite, created = None, False
        if event_type == 'online':
            favorite, created = Favorite.objects.get_or_create(user=request.user, online=event)
        elif event_type == 'offline':
            favorite, created = Favorite.objects.get_or_create(user=request.user, offline=event)
        elif event_type == 'attractions':
            favorite, created = Favorite.objects.get_or_create(user=request.user, attractions=event)
        elif event_type == 'for_visiting':
            favorite, created = Favorite.objects.get_or_create(user=request.user, for_visiting=event)

        if not created:
            favorite.delete()
            added = False
        else:
            added = True

        return JsonResponse({'added': added})

    return JsonResponse({'error': 'Event not found or user not authenticated'}, status=400)

# @login_required
# def events_add(request, event_slug):
#     try:
#         event = Events_online.objects.get(slug=event_slug)
#         event_type = 'online'
#     except Events_online.DoesNotExist:
#         try:
#             event = Events_offline.objects.get(slug=event_slug)
#             event_type = 'offline'
#         except Events_offline.DoesNotExist:
#             try:
#                 event = Attractions.objects.get(slug=event_slug)
#                 event_type = 'attractions'
#             except Attractions.DoesNotExist:
#                 try:
#                     event = Events_for_visiting.objects.get(slug=event_slug)
#                     event_type = 'for_visiting'
#                 except Events_for_visiting.DoesNotExist:
#                     event = None
#                     event_type = None

    # if event and request.user.is_authenticated:
    #     if event_type == 'online':
    #         Favorite.objects.get_or_create(user=request.user, online=event)
    #     elif event_type == 'offline':
    #         Favorite.objects.get_or_create(user=request.user, offline=event)
    #     elif event_type == 'attractions':
    #         Favorite.objects.get_or_create(user=request.user, attractions=event)
    #     elif event_type == 'for_visiting':
    #         Favorite.objects.get_or_create(user=request.user, for_visiting=event)

    # return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def events_remove(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Favorite, id=event_id, user=request.user)
        event.delete()
        return JsonResponse({'removed': True})
    return JsonResponse({'removed': False, 'error': 'Invalid request method'}, status=400)

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
                    pass

    if event and request.user.is_authenticated:
        favorite, created = None, False
        if event_type == 'online':
            favorite, created = Registered.objects.get_or_create(user=request.user, online=event)
        elif event_type == 'offline':
            favorite, created = Registered.objects.get_or_create(user=request.user, offline=event)
        elif event_type == 'attractions':
            favorite, created = Registered.objects.get_or_create(user=request.user, attractions=event)
        elif event_type == 'for_visiting':
            favorite, created = Registered.objects.get_or_create(user=request.user, for_visiting=event)
        
        if not created:
            favorite.delete()
            added = False
        else:
            added = True

        return JsonResponse({'added': added})

    return JsonResponse({'error': 'Event not found or user not authenticated'}, status=400)

  

@login_required
def registered_remove(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Registered, id=event_id, user=request.user)
        event.delete()
        return JsonResponse({'removed': True})
    return JsonResponse({'removed': False, 'error': 'Invalid request method'}, status=400)



@login_required
def registered(request):
    registered = Registered.objects.filter(user=request.user)
    context = {'favorites': registered}
    return render(request, 'bookmarks/registered.html', context)