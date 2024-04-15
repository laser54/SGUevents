from django.shortcuts import render

from events_cultural.models import Attractions, Events_for_visiting

def attractions(request):
	attractions_content= Attractions.objects.all()
	
	
	context: dict[str, str] = {
		'name_page': 'Достопримечательности',
        'event_card_views': attractions_content,
	}
	return render(request, 'events_cultural/attractions.html', context)


def events_for_visiting(request):
	events_for_visiting_content = Events_for_visiting.objects.all()

	context: dict[str, str] = {
		'name_page': 'Доступно к посещению',
		'event_card_views': events_for_visiting_content,
	}
	return render(request, 'events_cultural/events_for_visiting.html', context)


def events_registered(request):
	context: dict[str, str] = {
			'name_page': 'Зарегистрированные мероприятия',
	}
	return render(request, 'events_cultural/events_registered.html', context)

def index(request):
	return render(request, 'events_cultural/index.html')
