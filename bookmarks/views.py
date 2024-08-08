from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from bookmarks.models import Favorite, Registered
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting, Review
from users.telegram_utils import send_message_to_user
from events_cultural.views import submit_review
from django.views.decorators.csrf import csrf_exempt

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

        return JsonResponse({'added': added, 'event_id': favorite.id})

    return JsonResponse({'error': 'Event not found or user not authenticated'}, status=400)

@login_required
def events_remove(request, event_id):
    if request.method == 'POST':
        favorite = get_object_or_404(Favorite, id=event_id, user=request.user)
        favorite.delete()
        return JsonResponse({'removed': True})
    return JsonResponse({'removed': False, 'error': 'Invalid request method'}, status=400)

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_timestamp')

    events = []
    for fav in favorites:
        if fav.online:
            events.append(fav.online)
        elif fav.offline:
            events.append(fav.offline)
        elif fav.attractions:
            events.append(fav.attractions)
        elif fav.for_visiting:
            events.append(fav.for_visiting)
    
    reviews = {}
    for event in events:
        content_type = ContentType.objects.get_for_model(event)
        reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    events_for_visiting = [event for event in events if isinstance(event, Events_for_visiting)]
    registered = Registered.objects.filter(user=request.user, for_visiting__in=events_for_visiting)
    registered_dict = {reg.for_visiting.id: reg.id for reg in registered}

    context = {
        'events': events,
        'reviews': reviews,
        'favorites': favorites,
        'registered': registered_dict,
    }
    return render(request, 'bookmarks/favorites.html', context)

def events_attended(request):
    pass
    return render(request, "bookmarks/events_attended.html")

@login_required
def events_registered(request, event_slug):
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
        registered, created = None, False
        if event_type == 'online':
            registered, created = Registered.objects.get_or_create(user=request.user, online=event)
        elif event_type == 'offline':
            registered, created = Registered.objects.get_or_create(user=request.user, offline=event)
        elif event_type == 'attractions':
            registered, created = Registered.objects.get_or_create(user=request.user, attractions=event)
        elif event_type == 'for_visiting':
            registered, created = Registered.objects.get_or_create(user=request.user, for_visiting=event)

        if created:
            return JsonResponse({'added': True, 'event_id': registered.id, 'event_slug': event_slug})
        else:
            return JsonResponse({'added': False, 'error': 'Already registered'}, status=400)

    return JsonResponse({'error': 'Event not found or user not authenticated'}, status=400)

@login_required
def registered_remove(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Registered, id=event_id, user=request.user)
        event_slug = event.for_visiting.slug if event.for_visiting else (
            event.online.slug if event.online else (
                event.offline.slug if event.offline else (
                    event.attractions.slug if event.attractions else None
                )
            )
        )
        event.delete()
        telegram_id = request.user.telegram_id
        if telegram_id:
            message = f"Вы успешно отменили регистрацию на мероприятие: {event_slug}"
            send_message_to_user(telegram_id, message)
        return JsonResponse({'removed': True, 'event_slug': event_slug})
    return JsonResponse({'removed': False, 'error': 'Invalid request method'}, status=400)

@login_required
def registered(request):
    registered = Registered.objects.filter(user=request.user)
    reviews = {}
    events = []
    for reg in registered:
        if reg.online:
            events.append(reg.online)
        elif reg.offline:
            events.append(reg.offline)
        elif reg.attractions:
            events.append(reg.attractions)
        elif reg.for_visiting:
            events.append(reg.for_visiting)
    
    for event in events:
        content_type = ContentType.objects.get_for_model(event)
        reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'registered': registered,
        'reviews': reviews,
    }
    return render(request, 'bookmarks/registered.html', context)

@login_required
@csrf_exempt
def submit_review(request, event_id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        model_type = request.POST.get('model_type', '')

        if not comment:
            return JsonResponse({'success': False, 'message': 'Комментарий не может быть пустым'})

        if model_type == 'online':
            event = get_object_or_404(Events_online, id=event_id)
        elif model_type == 'offline':
            event = get_object_or_404(Events_offline, id=event_id)
        else:
            return JsonResponse({'success': False, 'message': 'Некорректный тип мероприятия'}, status=400)

        content_type = ContentType.objects.get_for_model(event)
        review = Review.objects.create(
            user=request.user,
            content_type=content_type,
            object_id=event.id,
            comment=comment
        )
        return JsonResponse({
            'success': True,
            'message': 'Отзыв добавлен',
            'formatted_date': review.formatted_date()
        })
    return JsonResponse({'success': False, 'message': 'Некорректный запрос'}, status=400)


