from events_available.models import Events_online, Events_offline
from django.db.models import Q

def q_search_online(query):
	if query.isdigit() and len(query) <= 5:
		return Events_online.objects.filter(id=int(query))
	
	return Events_online.objects.filter(description__search=query)

	# keyword = [word for word in query.split() if len(word) > 2]

	# q_objects = Q()
	# for token in keyword:
	# 	q_objects |= Q(description__icontains=token)
	# 	q_objects |= Q(name__icontains=token)


	# return Events_online.objects.filter(q_objects)
	
def q_search_offline(query):
	if query.isdigit() and len(query) <= 5:
		return Events_offline.objects.filter(id=int(query))