from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from bookmarks.models import Favorite
from events_available.models import *
from events_cultural.models import *
from main.models import AllEvents
from main.utils import q_search_all
from itertools import chain
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    available = Events_online.objects.order_by('date')
    available1 = Events_offline.objects.order_by('date')
    cultural = Attractions.objects.order_by('date')
    cultural1 = Events_for_visiting.objects.order_by('date')
    all_content = list(chain(available, available1, cultural, cultural1))

    page = request.GET.get('page', 1)
    f_all = request.GET.get('f_all', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if not query:
        events_all = Events_online.objects.order_by('time_start')
    else:
        events_all = q_search_all(query)

    if f_all:
        events_all = events_all.filter(date__month=1)
    
    if order_by and order_by != "default":
        events_all = events_all.order_by(order_by)

    paginator = Paginator(all_content, 10)
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

    context = {
        'name_page': 'Главная',
        'event_card_views': current_page,
        'favorites': favorites_dict,
        'check': 1,
    }

    return render(request, 'main/index.html', context)


	
    
    
    

    

    
	
	