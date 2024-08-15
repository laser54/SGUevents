from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from bookmarks.models import Favorite, Registered
from events_available.models import Events_offline, Events_online
from events_cultural.models import Attractions, Events_for_visiting, Review
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from main.utils import q_search_all

@login_required
def index(request):
    available = Events_online.objects.order_by('date')
    available1 = Events_offline.objects.order_by('date')
    cultural = Attractions.objects.order_by('date')
    cultural1 = Events_for_visiting.objects.order_by('date')
    user = request.user

    if user.is_superuser or user.department.department_name not in ['Administration', 'Superuser']:
        all_content = list(chain(available, available1, cultural, cultural1))
    else:
        if user.department:
            available = available.filter(Q(secret__isnull=True) | Q(secret=user.department)).distinct()
            available1 = available1.filter(Q(secret__isnull=True) | Q(secret=user.department)).distinct()
            cultural = cultural.filter(Q(secret__isnull=True) | Q(secret=user.department)).distinct()
            cultural1 = cultural1.filter(Q(secret__isnull=True) | Q(secret=user.department)).distinct()
        else:
            available = available.filter(secret__isnull=True).distinct()
            available1 = available1.filter(secret__isnull=True).distinct()
            cultural = cultural.filter(secret__isnull=True).distinct()
            cultural1 = cultural1.filter(secret__isnull=True).distinct()
        
        all_content = list(chain(available, available1, cultural, cultural1))

    page = request.GET.get('page', 1)
    f_all = request.GET.get('f_all', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if not query:
        events_all = all_content
    else:
        events_all = q_search_all(query)

    if f_all:
        events_all = [event for event in events_all if event.date.month == 1]
    
    if order_by and order_by != "default":
        events_all = sorted(events_all, key=lambda x: getattr(x, order_by))

    paginator = Paginator(events_all, 10)
    current_page = paginator.page(int(page))

    current_online = [event for event in current_page if isinstance(event, Events_online)]
    current_offline = [event for event in current_page if isinstance(event, Events_offline)]
    current_attractions = [event for event in current_page if isinstance(event, Attractions)]
    current_for_visiting = [event for event in current_page if isinstance(event, Events_for_visiting)]

    favorites_online = Favorite.objects.filter(user=request.user, online__in=current_online).values_list('online_id', 'id')
    favorites_offline = Favorite.objects.filter(user=request.user, offline__in=current_offline).values_list('offline_id', 'id')
    favorites_attractions = Favorite.objects.filter(user=request.user, attractions__in=current_attractions).values_list('attractions_id', 'id')
    favorites_for_visiting = Favorite.objects.filter(user=request.user, for_visiting__in=current_for_visiting).values_list('for_visiting_id', 'id')

    favorites_dict = {
        'online': {item[0]: item[1] for item in favorites_online},
        'offline': {item[0]: item[1] for item in favorites_offline},
        'attractions': {item[0]: item[1] for item in favorites_attractions},
        'for_visiting': {item[0]: item[1] for item in favorites_for_visiting},
    }

    registered_online = Registered.objects.filter(user=request.user, online__in=current_online).values_list('online_id', 'id')
    registered_offline = Registered.objects.filter(user=request.user, offline__in=current_offline).values_list('offline_id', 'id')
    registered_attractions = Registered.objects.filter(user=request.user, attractions__in=current_attractions).values_list('attractions_id', 'id')
    registered_for_visiting = Registered.objects.filter(user=request.user, for_visiting__in=current_for_visiting).values_list('for_visiting_id', 'id')

    registered_dict = {
        'online': {item[0]: item[1] for item in registered_online},
        'offline': {item[0]: item[1] for item in registered_offline},
        'attractions': {item[0]: item[1] for item in registered_attractions},
        'for_visiting': {item[0]: item[1] for item in registered_for_visiting},
    }
    
    reviews = {}
    for event in current_page:
        content_type = ContentType.objects.get_for_model(event)
        reviews[event.unique_id] = Review.objects.filter(content_type=content_type, object_id=event.id)

    context = {
        'name_page': 'Главная',
        'event_card_views': current_page,
        'favorites': favorites_dict,
        'reviews': reviews,
        'registered': registered_dict,
    }

    return render(request, 'main/index.html', context)