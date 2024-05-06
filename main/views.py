from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from events_available.models import *
from events_cultural.models import *

def index(request):
	page = request.GET.get('page',1)
	available=  Events_online.objects.order_by('date')
	available1 = Events_offline.objects.order_by('date')
	cultural = Attractions.objects.order_by('date')
	cultural1 = Events_for_visiting.objects.order_by('date')
	all_content = list(available) + list(available1) + list(cultural) + list(cultural1)
	paginator = Paginator(all_content, 4)
	current_page = paginator.page(int(page))
	context: dict[str, str] = {
		'name_page': 'Все мероприятия',
        'event_card_views': current_page,
		
	}
	
	return render(request, 'main/index.html', context)

