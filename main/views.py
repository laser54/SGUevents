from django.shortcuts import render

def index(request):
	context: dict[str, str] = {
		'title': 'Home - Главная',
		'content': 'Мероприятия'
	}
	return render(request, 'main/index.html', context)

