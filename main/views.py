from django.shortcuts import render
from events_available.models import *
from events_cultural.models import *

def index(request):
	available=  Events_online.objects.all()
	available1 = Events_offline.objects.all()
	cultural = Attractions.objects.all()
	cultural1 = Events_for_visiting.objects.all()
	all_content = list(available) + list(available1) + list(cultural) + list(cultural1)
	context: dict[str, str] = {
		'name_page': 'Все мероприятия',
        'event_card_views': all_content,
		
	}
	
	return render(request, 'main/index.html', context)

