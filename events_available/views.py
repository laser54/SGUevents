from django.shortcuts import get_list_or_404, get_object_or_404, render
from bookmarks.models import Favorite
from events_available.models import Events_offline, Events_online
from django.core.paginator import Paginator
from events_available.utils import q_search_offline, q_search_online, q_search_name_offline
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def online(request):
	page = request.GET.get('page',1)
	f_date = request.GET.get('f_date', None)
	f_speakers = request.GET.get('f_speakers', None)
	f_tags = request.GET.get('f_tags', None)
	order_by = request.GET.get('order_by', None)
	date_start = request.GET.get('date_start', None)
	date_end = request.GET.get('date_end', None)
	time_to_start = request.GET.get('time_to_start', None)
	time_to_end = request.GET.get('time_to_end',None)
	query = request.GET.get('q', None)
	
	all_info = Events_online.objects.all()
	speakers_info = [event.speakers for event in all_info]
	speakers = []
	for name in speakers_info:
		names_list = name.split()
		for i in range(0,len(names_list),3):
			speakers.append(' '.join(names_list[i:i+3]))

	if not query:
		events_available = Events_online.objects.order_by('date')
	else:
		events_available = q_search_online(query)

	if f_date:
		events_available = events_available.filter(date__month = 1)

	if f_speakers:
		events_available = Events_online.objects.filter(speakers__icontains=f_speakers)
	
	tags = [event.tags for event in all_info]

	if f_tags:
		events_available = Events_online.objects.filter(tags__icontains=f_tags)
	
	if order_by and order_by != "default":
		events_available = events_available.order_by(order_by)

	if date_start:
		date_start_formatted = datetime.strptime(date_start, '%Y-%m-%d').date()
		events_available = events_available.filter(date__gt = date_start_formatted)

	if date_end:
		date_end_formatted = datetime.strptime(date_end, '%Y-%m-%d').date()
		events_available = events_available.filter(date__lt = date_end_formatted)

	# if time_to_start:
	# 	events_available = events_available.filter(time_start__time__gte = time_to_start)
    

	
	# event = Events_online.objects.get(id=events_id)


	paginator = Paginator(events_available, 3)
	current_page = paginator.page(int(page))

	favorites = Favorite.objects.filter(user=request.user, online__in=current_page).values_list('online_id', flat=True)


	context: dict[str, str] = {
			'name_page': 'Онлайн',
            'event_card_views': current_page,
			'speakers': speakers,
			'tags': tags,
			'favorites': list(favorites),
						
			# 'slug_url': event_slug
	}
	return render(request, 'events_available/online_events.html', context=context)

@login_required
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

@login_required
def offline(request):
	page = request.GET.get('page',1)
	f_date = request.GET.get('f_date', None)
	f_speakers = request.GET.get('f_speakers', None)
	f_tags = request.GET.get('f_tags', None)
	order_by = request.GET.get('order_by', None)
	query = request.GET.get('q', None)
	query_name = request.GET.get('qn', None)
	date_start = request.GET.get('date_start', None)
	date_end = request.GET.get('date_end', None)


	all_info = Events_offline.objects.all()
	speakers_info = [event.speakers for event in all_info]
	speakers = []
	for name in speakers_info:
		names_list = name.split()
		for i in range(0,len(names_list),3):
			speakers.append(' '.join(names_list[i:i+3]))

	if not query_name:
		events_available = Events_offline.objects.order_by('time_start')
	else:
		events_available = q_search_name_offline(query_name)

	if not query:
		events_available = events_available.order_by('time_start')
	else:
		events_available = q_search_offline(query)

	if f_date:
		events_available = events_available.filter(date__month = 1)

	if date_start:
		date_start_formatted = datetime.strptime(date_start, '%Y-%m-%d').date()
		events_available = events_available.filter(date__gt = date_start_formatted)

	if date_end:
		date_end_formatted = datetime.strptime(date_end, '%Y-%m-%d').date()
		events_available = events_available.filter(date__lt = date_end_formatted)
	
	if f_speakers:
		events_available = Events_offline.objects.filter(speakers__icontains=f_speakers)

	tags = [event.tags for event in all_info]

	if f_tags:
		events_available = Events_offline.objects.filter(tags__icontains=f_tags)
	
	if order_by and order_by != "default":
		events_available = events_available.order_by(order_by)

	if date_start:
		date_start_formatted = datetime.strptime(date_start, '%Y-%m-%d').date()
		events_available = events_available.filter(date__gt = date_start_formatted)

	if date_end:
		date_end_formatted = datetime.strptime(date_end, '%Y-%m-%d').date()
		events_available = events_available.filter(date__lt = date_end_formatted)

	paginator = Paginator(events_available, 3)
	current_page = paginator.page(int(page))

	context: dict[str, str] = {
        'name_page': 'Оффлайн',
		'event_card_views': current_page,
		'speakers': speakers,
		'tags': tags,
    }
	return render(request, 'events_available/offline_events.html', context)

@login_required
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


    