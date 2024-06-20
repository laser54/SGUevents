from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from bookmarks.models import Favorite
from events_available.models import Events_online, Events_offline
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_favorite(request, event_slug):
    try:
        event = Events_online.objects.get(slug=event_slug)
    except Events_online.DoesNotExist:
        event = get_object_or_404(Events_offline, slug=event_slug)

    favorite, created = Favorite.objects.get_or_create(user=request.user, event_online=event if isinstance(event, Events_online) else None, event_offline=event if isinstance(event, Events_offline) else None)

    if not created:
        favorite.delete()
        action = 'removed'
    else:
        action = 'added'

    if request.is_ajax():
        return JsonResponse({'status': 'success', 'action': action})
    else:
        return redirect('bookmarks:favorites')

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'bookmarks/favorites.html', {'favorites': favorites})

@login_required
def events_attended(request, event_slug=None):
    # Your logic for events_attended view
    pass
