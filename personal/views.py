from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import EventsOnlineForm, EventsOfflineForm

@login_required
def add_online_event(request):
    if request.method == 'POST':
        form = EventsOnlineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('personal:personal'))
    else:
        form = EventsOnlineForm()

    form_html = render_to_string('personal/event_form.html', {'form': form})
    return JsonResponse({'form_html': form_html})

@login_required
def add_offline_event(request):
    if request.method == 'POST':
        form = EventsOfflineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('personal:personal'))
    else:
        form = EventsOfflineForm()

    form_html = render_to_string('personal/event_form.html', {'form': form})
    return JsonResponse({'form_html': form_html})

@login_required
def personal(request):
    return render(request, 'personal/personal.html')
