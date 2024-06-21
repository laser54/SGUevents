from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from bookmarks.models import Product
from events_available.models import Events_online
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def events_attended(request):
	context: dict[str, str] = {
        'name_page': 'Посещенные мероприятия',
		'1_event_attended_title': 'Первое название посещенного мероприятия',
		'1_event_attended_info': 'Информация про посещенные мероприятия',
		'2_event_attended_title': 'Второе название посещенного мероприятия',
		'2_event_attended_info': 'Информация про посещенные мероприятия',
		'3_event_attended_title': 'Третье название посещенного мероприятия',
		'3_event_attended_info': 'Информация про посещенные мероприятия',
		'4_event_attended_title': 'Четвёртое название посещенного мероприятия',
		'4_event_attended_info': 'Информация про посещенные мероприятия',
		'5_event_attended_title': 'Пятое название посещенного мероприятия',
		'5_event_attended_info': 'Информация про посещенные мероприятия',
		'6_event_attended_title': 'Шестое название посещенного мероприятия',
		'6_event_attended_info': 'Информация про посещенные мероприятия'
    }
	
	return render(request, 'bookmarks/events_attended.html', context)

@login_required
def favorites(request, event_slug=False):
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
        
    # }
    # if request.is_ajax():
    #     html = render_to_string('favorites.html', context, request=request) # type: ignore
    #     return JsonResponse({'form': html})
    return render(request, 'bookmarks/favorites.html')


class AddToFavourite(LoginRequiredMixin, ListView):
    template_name = "AddToFavourite.html"
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'product_list'
    
    def get_context_data(self, **kwargs):
        context = super(AddToFavourite, self).get_context_data(**kwargs)
        product_item = get_object_or_404(Product, slug=self.kwargs['event_slug']) # how to pass slug of each product item here?

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
