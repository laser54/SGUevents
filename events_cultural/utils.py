from events_cultural.models import Attractions, Events_for_visiting

def q_search_events_for_visiting(query):
	if query.isdigit() and len(query) <= 5:
		return Events_for_visiting.objects.filter(id=int(query))
	
def q_search_attractions(query):
	if query.isdigit() and len(query) <= 5:
		return Attractions.objects.filter(id=int(query))