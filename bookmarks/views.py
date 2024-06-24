from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from bookmarks.models import Favorite
from events_available.models import Events_online
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def events_attended(request, event_slug):
    events = Events_online.objects.get(slug=event_slug)

    if request.user.is_authenticated:
        events_f = Favorite.objects.filter(user=request.user, online=events)
        Favorite.objects.create(user=request.user, online=events)
        # if events_f.exists():
        #     events_f = events_f.first()
        #     if cart:
        #         cart.quantity += 1
        #         cart.save()
        # else:
            
	# context: dict[str, str] = {
       
    # }
    return redirect(request.META['HTTP_REFERER'])

@login_required
def favorites(request, event_slug=False):
    # events = Favorite.objects.all()
    # context = { 
    #     'event_card_views': events,
    
    # }
    # product = get_object_or_404(Product, slug=event_slug)
    # added_to_favourite = False
    # if product.favourite.filter(id=request.user.id).exists():
    #     product.favourite.remove(request.user)
    #     added_to_favourite = False
    # else:
    #     product.favourite.add(request.user)
    #     added_to_favourite = True

    # context = {
    #     'object': product,
    #     'added_to_favourite': added_to_favourite,
    # context = {
    #     'object': product,
    #     'added_to_favourite': added_to_favourite,
        
    # }
    # if request.is_ajax():
    #     html = render_to_string('favorites.html', context, request=request) # type: ignore
    #     return JsonResponse({'form': html})
    
    return render(request, 'bookmarks/favorites.html')


class AddToFavourite(LoginRequiredMixin, ListView):
    template_name = "AddToFavourite.html"
    model = Favorite
    queryset = Favorite.objects.all()
    context_object_name = 'product_list'
    
    def get_context_data(self, **kwargs):
        context = super(AddToFavourite, self).get_context_data(**kwargs)
        product_item = get_object_or_404(Favorite, slug=self.kwargs['event_slug']) # how to pass slug of each product item here?

        added_to_favourite = False
        if product_item.cart.filter(id=self.request.user.id).exists():
            added_to_favourite = True
        
        context['added_to_favourite'] = added_to_favourite
        
		# page = request.GET.get('page',1)
		
		# fav = Events_online.objects.all()

		# paginator = Paginator(fav, 3)
		# current_page = paginator.page(int(page))

		# context: dict[str, str] = {
		# 		'name_page': 'Онлайн',
		# 		'event_card_views': current_page,
		# }

		# return render(request, 'bookmarks/events_attended.html', context)

@login_required
def index(request):
	return render(request, 'bookmarks/index.html')
