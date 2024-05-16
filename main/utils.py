from events_available.models import *
from events_cultural.models import *
from main.models import AllEvents
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline
from itertools import chain

def q_search_all(query):
	if query.isdigit() and len(query) <= 5:
		return Events_online.objects.filter(id=int(query))
	
	vector = SearchVector("name", "description")
	query = SearchQuery(query)
	# available=  Events_online.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
	# available1 = Events_offline.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
	# cultural = Attractions.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
	# cultural1 = Events_for_visiting.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")

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