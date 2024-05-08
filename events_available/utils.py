from events_available.models import Events_online, Events_offline

def q_search_online(query):
	if query.isdigit() and len(query) <= 5:
		return Events_online.objects.filter(id=int(query))
	
def q_search_offline(query):
	if query.isdigit() and len(query) <= 5:
		return Events_offline.objects.filter(id=int(query))