from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from events_available.models import *
from events_cultural.models import *
from main.models import AllEvents
from main.utils import q_search_all
from itertools import chain

def index(request):
	available=  Events_online.objects.order_by('date')
	available1 = Events_offline.objects.order_by('date')
	cultural = Attractions.objects.order_by('date')
	cultural1 = Events_for_visiting.objects.order_by('date')
	all_content = list(chain(available, available1, cultural, cultural1))

	page = request.GET.get('page',1)
	f_all = request.GET.get('f_all', None)
	order_by = request.GET.get('order_by', None)
	query = request.GET.get('q', None)

	if not query:
		# events_all = AllEvents.objects.order_by('time_start')
		events_all = Events_online.objects.order_by('time_start')
	else:
		events_all = q_search_all(query)

	if f_all:
		events_all = events_all.filter(date__month = 1)
	
	if order_by and order_by != "default":
		events_all = events_all.order_by(order_by)

	
	paginator = Paginator(all_content, 10)
	current_page = paginator.page(int(page))
	context: dict[str, str] = {
		'name_page': 'Все мероприятия',
        'event_card_views': current_page,
		
	}
	
	return render(request, 'main/index.html', context)

