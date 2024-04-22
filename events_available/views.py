from django.shortcuts import render
from django.core.paginator import Paginator
from events_available.models import Events_offline, Events_online

def online(request, page=1):
	events_available = Events_online.objects.all()
	# event = Events_online.objects.get(id=events_id)
	
	paginator = Paginator(events_available, 3)
	current_page = paginator.page(page)


	context: dict[str, str] = {
			'name_page': 'Онлайн',
            'event_card_views': current_page,
			# 'pere': event
	}
	return render(request, 'events_available/online_events.html', context=context)

def online_card(request, event_slug=False, event_id=False):
	event = Events_online.objects.all()
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
    
	events_available = Events_offline.objects.all()

	context: dict[str, str] = {
        'name_page': 'Оффлайн',
		'event_card_views': events_available
    }
	return render(request, 'events_available/offline_events.html', context)


def offline_card(request, event_slug=False, event_id=False):
	event = Events_offline.objects.all()
	# event = Events_online.objects.get(id=events_id)
	if event_id:
		event = Events_offline.objects.get(id=event_id)
	else:
		event = Events_offline.objects.get(slug=event_slug)

	context: dict[str, str] = {
			'event': event,
	}

	return render(request, 'events_available/card.html', context=context)


    