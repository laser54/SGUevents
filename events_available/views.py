from django.shortcuts import render

from events_available.models import Events_offline, Events_online

def online(request):
	events_available = Events_online.objects.all()
	# event = Events_online.objects.get(id=events_id)
	
	context: dict[str, str] = {
			'name_page': 'Онлайн',
            'event_card_views': events_available,
			# 'pere': event
	}
	return render(request, 'events_available/online_events.html', context=context)

def online_card(request, events_id):
	event = Events_online.objects.all()
	# event = Events_online.objects.get(id=events_id)
	context: dict[str, str] = {
			'event_card_views': event,
	}

	return render(request, 'events_available/card.html', context=context)



def offline(request):
    
	events_available = Events_offline.objects.all()

	context: dict[str, str] = {
        'name_page': 'Оффлайн',
		'event_card_views': events_available
    }
	return render(request, 'events_available/offline_events.html', context)


    