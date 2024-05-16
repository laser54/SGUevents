from events_available.models import Events_online, Events_offline
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline

def q_search_online(query):
	if query.isdigit() and len(query) <= 5:
		return Events_online.objects.filter(id=int(query))
	
	vector = SearchVector("name", "description")
	query = SearchQuery(query)
	result = Events_online.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
	
	result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

	# result = result.annotate(
    #     bodyline=SearchHeadline(
    #         "description",
    #         query,
    #         start_sel='<span style="background-color: yellow;">',
    #         stop_sel="</span>",
    #     )
    # )
	return result

    
	# keyword = [word for word in query.split() if len(word) > 2]

	# q_objects = Q()
	# for token in keyword:
	# 	q_objects |= Q(description__icontains=token)
	# 	q_objects |= Q(name__icontains=token)


	# return Events_online.objects.filter(q_objects)
	
def q_search_offline(query):
	if query.isdigit() and len(query) <= 5:
		return Events_offline.objects.filter(id=int(query))