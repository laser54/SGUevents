from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from events_cultural.models import Attractions, Events_for_visiting
from events_cultural.utils import q_search_events_for_visiting, q_search_attractions

def attractions(request):
	page = request.GET.get('page',1)
	f_attractions = request.GET.get('f_attractions', None)
	order_by = request.GET.get('order_by', None)
	query = request.GET.get('q', None)
	
	if not query:
		events_cultural = Attractions.objects.order_by('time_start')
	else:
		events_cultural = q_search_attractions(query)

	if f_attractions:
		events_cultural = events_cultural.filter(date__month = 1)
	
	if order_by and order_by != "default":
		events_cultural = events_cultural.order_by(order_by)

	
	paginator = Paginator(events_cultural, 3)
	current_page = paginator.page(int(page))
	
	context: dict[str, str] = {
		'name_page': 'Достопримечательности',
        'event_card_views': current_page,
	}
	return render(request, 'events_cultural/attractions.html', context)

def attractions_card(request, event_slug=False, event_id=False):
	event = Attractions.objects.all()

	if event_id:
		event = Attractions.objects.get(id=event_id)
	else:
		event = Attractions.objects.get(slug=event_slug)

	context: dict[str, str] = {
			'event': event,
	}

	return render(request, 'events_cultural/card.html', context=context)

def events_for_visiting(request):
	page = request.GET.get('page',1)
	f_events_for_visiting = request.GET.get('f_events_for_visiting', None)
	order_by = request.GET.get('order_by', None)
	query = request.GET.get('q', None)

	if not query:
		events_cultural = Events_for_visiting.objects.order_by('time_start')
	else:
		events_cultural = q_search_events_for_visiting(query)

	if f_events_for_visiting:
		events_cultural = events_cultural.filter(date__month = 1)
	
	if order_by and order_by != "default":
		events_cultural = events_cultural.order_by(order_by)

	paginator = Paginator(events_cultural, 3)
	current_page = paginator.page(int(page))

	context: dict[str, str] = {
		'name_page': 'Доступные к посещению',
		'event_card_views': current_page,
	}
	return render(request, 'events_cultural/events_for_visiting.html', context)

def for_visiting_card(request, event_slug=False, event_id=False):
	event = Events_for_visiting.objects.all()
	
	if event_id:
		event = Events_for_visiting.objects.get(id=event_id)
	else:
		event = Events_for_visiting.objects.get(slug=event_slug)

	context: dict[str, str] = {
			'event': event,
	}

	return render(request, 'events_cultural/card.html', context=context)

def events_registered(request):
	context: dict[str, str] = {
			'name_page': 'Зарегистрированные мероприятия',
	}
	return render(request, 'events_cultural/events_registered.html', context)

def index(request):
	return render(request, 'events_cultural/index.html')

# def registered_card(request, event_slug=False, event_id=False):
# 	event = Events_online.objects.all()
# 	# event = Events_online.objects.get(id=events_id)
# 	if event_id:
# 		event = Events_online.objects.get(id=event_id)
# 	else:
# 		event = Events_online.objects.get(slug=event_slug)

# 	context: dict[str, str] = {
# 			'event': event,
# 	}

# 	return render(request, 'events_cultural/card.html', context=context)