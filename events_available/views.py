from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from bookmarks.models import Favorite, Registered
from events_available.models import Events_offline, Events_online
from django.core.paginator import Paginator
from events_available.utils import q_search_offline, q_search_online, q_search_name_offline
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from events_cultural.models import Review

@login_required
def online(request):
    page = request.GET.get('page', 1)
    f_date = request.GET.get('f_date', None)
    f_speakers = request.GET.get('f_speakers', None)
    f_tags = request.GET.get('f_tags', None)
    order_by = request.GET.get('order_by', None)
    date_start = request.GET.get('date_start', None)
    date_end = request.GET.get('date_end', None)
    time_to_start = request.GET.get('time_to_start', None)
    time_to_end = request.GET.get('time_to_end', None)
    query = request.GET.get('q', None)

    all_info = Events_online.objects.all()
    speakers_info = [event.speakers for event in all_info]
    speakers = []
    for name in speakers_info:
        names_list = name.split()
        for i in range(0, len(names_list), 3):
            speakers.append(' '.join(names_list[i:i+3]))

    if not query:
        events_available = Events_online.objects.order_by('date')
    else:
        events_available = q_search_online(query)

    if f_date:
        events_available = events_available.filter(date__month=1)

    if f_speakers:
        events_available = Events_online.objects.filter(speakers__icontains=f_speakers)

    tags = [event.tags for event in all_info]

    if f_tags:
        events_available = events_available.filter(tags__icontains=f_tags)

    if order_by and order_by != "default":
        events_available = events_available.order_by(order_by)

    if date_start:
        date_start_formatted = datetime.strptime(date_start, '%Y-%m-%d').date()
        events_available = events_available.filter(date__gt=date_start_formatted)

    if date_end:
        date_end_formatted = datetime.strptime(date_end, '%Y-%m-%d').date()
        events_available = events_available.filter(date__lt=date_end_formatted)

    paginator = Paginator(events_available, 3)
    current_page = paginator.page(int(page))

    favorites = Favorite.objects.filter(user=request.user, online__in=current_page)
    favorites_dict = {favorite.online.id: favorite.id for favorite in favorites}

    registered = Registered.objects.filter(user=request.user, online__in=current_page)
    registered_dict = {reg.online.id: reg.id for reg in registered}

    reviews = {}
    for event in current_page:
        content_type = ContentType.objects.get_for_model(event)
        reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'name_page': 'Онлайн',
        'event_card_views': current_page,
        'speakers': speakers,
        'tags': tags,
        'favorites': favorites_dict,
        'registered': registered_dict,
        'reviews': reviews,
    }

    return render(request, 'events_available/online_events.html', context=context)

@login_required
def online_card(request, event_slug=False, event_id=False):
    if event_id:
        event = Events_online.objects.get(id=event_id)
    else:
        event = Events_online.objects.get(slug=event_slug)

    content_type = ContentType.objects.get_for_model(event)
    reviews = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'event': event,
        'reviews': reviews,
    }
    return render(request, 'events_available/card.html', context=context)

@login_required
def offline(request):
    page = request.GET.get('page', 1)
    f_date = request.GET.get('f_date', None)
    f_speakers = request.GET.get('f_speakers', None)
    f_tags = request.GET.get('f_tags', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    query_name = request.GET.get('qn', None)
    date_start = request.GET.get('date_start', None)
    date_end = request.GET.get('date_end', None)

    all_info = Events_offline.objects.all()
    speakers_info = [event.speakers for event in all_info]
    speakers = []
    for name in speakers_info:
        names_list = name.split()
        for i in range(0, len(names_list), 3):
            speakers.append(' '.join(names_list[i:i+3]))

    if not query_name:
        events_available = Events_offline.objects.order_by('time_start')
    else:
        events_available = q_search_name_offline(query_name)

    if not query:
        events_available = events_available.order_by('time_start')
    else:
        events_available = q_search_offline(query)

    if f_date:
        events_available = events_available.filter(date__month=1)

    if date_start:
        date_start_formatted = datetime.strptime(date_start, '%Y-%m-%d').date()
        events_available = events_available.filter(date__gt=date_start_formatted)

    if date_end:
        date_end_formatted = datetime.strptime(date_end, '%Y-%m-%d').date()
        events_available = events_available.filter(date__lt=date_end_formatted)

    if f_speakers:
        events_available = Events_offline.objects.filter(speakers__icontains=f_speakers)

    tags = [event.tags for event in all_info]

    if f_tags:
        events_available = Events_offline.objects.filter(tags__icontains=f_tags)

    if order_by and order_by != "default":
        events_available = events_available.order_by(order_by)

    paginator = Paginator(events_available, 3)
    current_page = paginator.page(int(page))

    favorites = Favorite.objects.filter(user=request.user, offline__in=current_page)
    favorites_dict = {favorite.offline.id: favorite.id for favorite in favorites}

    registered = Registered.objects.filter(user=request.user, offline__in=current_page)
    registered_dict = {reg.offline.id: reg.id for reg in registered}

    reviews = {}
    for event in current_page:
        content_type = ContentType.objects.get_for_model(event)
        reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'name_page': 'Оффлайн',
        'event_card_views': current_page,
        'speakers': speakers,
        'tags': tags,
        'favorites': favorites_dict,
        'registered': registered_dict,
        'reviews': reviews,
    }

    return render(request, 'events_available/offline_events.html', context=context)

@login_required
def offline_card(request, event_slug=False, event_id=False):
    if event_id:
        event = Events_offline.objects.get(id=event_id)
    else:
        event = Events_offline.objects.get(slug=event_slug)

    content_type = ContentType.objects.get_for_model(event)
    reviews = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'event': event,
        'reviews': reviews,
    }

    return render(request, 'events_available/card.html', context=context)

@login_required
@csrf_exempt
def submit_review(request, event_id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        model_type = request.POST.get('model_type', '')

        if not comment:
            return JsonResponse({'success': False, 'message': 'Комментарий не может быть пустым'})

        if model_type == 'offline':
            event = get_object_or_404(Events_offline, id=event_id)
        elif model_type == 'online':
            event = get_object_or_404(Events_online, id=event_id)
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
