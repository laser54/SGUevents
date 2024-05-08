from django.shortcuts import get_list_or_404, get_object_or_404, render
from events_available.models import Events_offline, Events_online
from django.core.paginator import Paginator
from events_available.utils import q_search_offline, q_search_online


def online(request):
	page = request.GET.get('page',1)
	f_online = request.GET.get('f_online', None)
	order_by = request.GET.get('order_by', None)
	query = request.GET.get('q', None)

	if not query:
		events_available = Events_online.objects.order_by('time_start')
	else:
		events_available = q_search_online(query)

	if f_online:
		events_available = events_available.filter(date__month = 1)
	
	if order_by and order_by != "default":
		events_available = events_available.order_by(order_by)
	# event = Events_online.objects.get(id=events_id)

	paginator = Paginator(events_available, 3)
	current_page = paginator.page(int(page))

	context: dict[str, str] = {
			'name_page': 'Онлайн',
            'event_card_views': current_page,
						
			# 'slug_url': event_slug
	}
	return render(request, 'events_available/online_events.html', context=context)

def online_card(request, event_slug=False, event_id=False):
	# event = Events_online.objects.all()
	# event = Events_online.objects.get(id=events_id)
	if event_id:
		event = Events_online.objects.get(id=event_id)
	else:
		event = Events_online.objects.get(slug=event_slug)

	context: dict[str, str] = {
			'event': event,
	}

	return render(request, 'events_available/card.html', context=context)



def offline(request):
	page = request.GET.get('page',1)
	f_offline = request.GET.get('f_offline', None)
	order_by = request.GET.get('order_by', None)
	query = request.GET.get('q', None)
    
	if not query:
		events_available = Events_offline.objects.order_by('time_start')
	else:
		events_available = q_search_offline(query)

	if f_offline:
		events_available = events_available.filter(date__month = 1)
	
	if order_by and order_by != "default":
		events_available = events_available.order_by(order_by)

	paginator = Paginator(events_available, 3)
	current_page = paginator.page(int(page))

	context: dict[str, str] = {
        'name_page': 'Оффлайн',
		'event_card_views': current_page,
    }
	return render(request, 'events_available/offline_events.html', context)


def offline_card(request, event_slug=False, event_id=False):
	# event = Events_offline.objects.all()
	# event = Events_online.objects.get(id=events_id)
	if event_id:
		event = Events_offline.objects.get(id=event_id)
	else:
		event = Events_offline.objects.get(slug=event_slug)

	context: dict[str, str] = {
			'event': event,
	}

	return render(request, 'events_available/card.html', context=context)


    