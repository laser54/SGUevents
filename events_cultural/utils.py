from events_cultural.models import Attractions, Events_for_visiting
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline

def q_search_events_for_visiting(query):
	if query.isdigit() and len(query) <= 5:
		return Events_for_visiting.objects.filter(id=int(query))
	
	vector = SearchVector("name", "description")
	query = SearchQuery(query)
	result = Events_for_visiting.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
	
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
	

	
def q_search_attractions(query):
	if query.isdigit() and len(query) <= 5:
		return Attractions.objects.filter(id=int(query))
	
	vector = SearchVector("name", "description")
	query = SearchQuery(query)
	result = Attractions.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
	
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
	
	