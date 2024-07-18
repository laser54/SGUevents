import json
from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from bookmarks.models import Favorite, Registered
from events_cultural.models import Attractions, Events_for_visiting, Review
from events_cultural.utils import q_search_events_for_visiting, q_search_attractions
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType

@login_required
def attractions(request):
    page = request.GET.get('page', 1)
    f_attractions = request.GET.get('f_attractions', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    
    if not query:
        events_cultural = Attractions.objects.order_by('time_start')
    else:
        events_cultural = q_search_attractions(query)

    if f_attractions:
        events_cultural = events_cultural.filter(date__month=1)
    
    if order_by and order_by != "default":
        events_cultural = events_cultural.order_by(order_by)

    paginator = Paginator(events_cultural, 3)
    current_page = paginator.page(int(page))

    # Получаем список избранных мероприятий для текущего пользователя
    favorites = Favorite.objects.filter(user=request.user, attractions__in=current_page)
    favorites_dict = {favorite.attractions.id: favorite.id for favorite in favorites}

    events = Attractions.objects.all()
    
    # Получение отзывов для каждого мероприятия
    reviews = {}
    for event in events:
        content_type = ContentType.objects.get_for_model(event)
        reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    
    context = {
        'name_page': 'Достопримечательности',
        'event_card_views': current_page,
        'favorites': favorites_dict,
        'reviews': reviews, 
    }
    return render(request, 'events_cultural/attractions.html', context)

@login_required
def attractions_card(request, event_slug=False, event_id=False):
    reviews = {}
    if event_id:
        event = Attractions.objects.get(id=event_id)
    else:
        event = Attractions.objects.get(slug=event_slug)

    content_type = ContentType.objects.get_for_model(event)
    reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'event': event,
        'reviews': reviews, 
    }
    return render(request, 'events_cultural/card.html', context=context)

@login_required
def events_for_visiting(request):
    page = request.GET.get('page', 1)
    f_events_for_visiting = request.GET.get('f_events_for_visiting', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if not query:
        events_cultural = Events_for_visiting.objects.order_by('time_start')
    else:
        events_cultural = q_search_events_for_visiting(query)

    if f_events_for_visiting:
        events_cultural = events_cultural.filter(date__month=1)
    
    if order_by and order_by != "default":
        events_cultural = events_cultural.order_by(order_by)

    paginator = Paginator(events_cultural, 3)
    current_page = paginator.page(int(page))

    # Получаем список избранных и зарегистрированных мероприятий для текущего пользователя
    favorites = Favorite.objects.filter(user=request.user, for_visiting__in=current_page)
    favorites_dict = {favorite.for_visiting.id: favorite.id for favorite in favorites}

    registered = Registered.objects.filter(user=request.user, for_visiting__in=current_page)
    registered_dict = {reg.for_visiting.id: reg.id for reg in registered}

    context = {
        'name_page': 'Доступные к посещению',
        'event_card_views': current_page,
        'favorites': favorites_dict,
        'registered': registered_dict,
    }
    return render(request, 'events_cultural/events_for_visiting.html', context)


@login_required
def for_visiting_card(request, event_slug=False, event_id=False):
    if event_id:
        event = Events_for_visiting.objects.get(id=event_id)
    else:
        event = Events_for_visiting.objects.get(slug=event_slug)

    context = {
        'event': event,
    }
    return render(request, 'events_cultural/card.html', context=context)

from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def submit_review(request, event_id):
    if request.method == 'POST':
        try:
            event = get_object_or_404(Attractions, id=event_id)
            comment = request.POST.get('comment', '')
            if comment:
                review = Review.objects.create(user=request.user, event=event, comment=comment)
                return JsonResponse({
                    'success': True,
                    'message': 'Отзыв добавлен',
                    'formatted_date': review.formatted_date()
                })
            else:
                return JsonResponse({'success': False, 'message': 'Комментарий не может быть пустым'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Некорректный запрос'}, status=400)


@login_required
def index(request):
    return render(request, 'events_cultural/index.html')
