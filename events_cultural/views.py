from django.shortcuts import render
from django.core.paginator import Paginator
from events_cultural.models import Attractions, Events_for_visiting

def attractions(request):
	page = request.GET.get('page',1)
	attractions_content= Attractions.objects.all()
	
	paginator = Paginator(attractions_content, 2)
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
	events_for_visiting_content = Events_for_visiting.objects.all()

	paginator = Paginator(events_for_visiting_content, 2)
	current_page = paginator.page(int(page))

	context: dict[str, str] = {
		'name_page': 'Доступно к посещению',
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