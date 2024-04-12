from django.shortcuts import render

from events_cultural.models import Attractions, Events_for_visiting

def attractions(request):
	attractions = Attractions.objects.all()
	
	
	context: dict[str, str] = {
		'name_page': 'Онлайн',
        'attractions': attractions,
		'name_page': 'Достопримечательности',
		'1_attractions_title': 'Первое название достопремичательности',
		'1_attractions_info': 'Каждый первый объект будет иметь свое описание',
		'2_attractions_title': 'Второе название достопремичательности',
		'2_attractions_info': 'Каждый второй объект будет иметь свое описание',
		'3_attractions_title': 'Третье название достопремичательности',
		'3_attractions_info': 'Каждый третий объект будет иметь свое описание',
		'4_attractions_title': 'Четвёртое название достопремичательности',
		'4_attractions_info': 'Каждый четвертый объект будет иметь свое описание',
		'5_attractions_title': 'Пятое название достопремичательности',
		'5_attractions_info': 'Каждый пятый ',
		'6_attractions_title': 'Шестое название достопремичательности',
		'6_attractions_info': 'Каждый шестой объект будет иметь свое описание'
	}
	return render(request, 'events_cultural/attractions.html', context)


def events_for_visiting(request):
	context: dict[str, str] = {
			'name_page': 'Доступно к посещению',
		'1_events_for_visiting_title': 'Первое название мероприятия, доступного к посещению',
		'1_events_for_visiting_info': 'Каждый первый объект будет иметь свое описание',
		'2_events_for_visiting_title': 'Второе название мероприятия, доступного к посещению',
		'2_events_for_visiting_info': 'Каждый второй объект будет иметь свое описание',
		'3_events_for_visiting_title': 'Третье название мероприятия, доступного к посещению',
		'3_events_for_visiting_info': 'Каждый третий объект будет иметь свое описание',
		'4_events_for_visiting_title': 'Четвёртое название мероприятия, доступного к посещению',
		'4_events_for_visiting_info': 'Каждый четвертый объект будет иметь свое описание',
		'5_events_for_visiting_title': 'Пятое название мероприятия, доступного к посещению',
		'5_events_for_visiting_info': 'Каждый пятый объект будет иметь свое описание',
		'6_events_for_visiting_title': 'Шестое название  мероприятия, доступного к посещению',
		'6_events_for_visiting_info': 'Каждый шестой объект будет иметь свое описание'
	}
	return render(request, 'events_cultural/events_for_visiting.html', context)


def events_registered(request):
	context: dict[str, str] = {
			'name_page': 'Зарегистрированные мероприятия',
		'1_events_registered_title': 'Первое название зарегистрированного мероприятия',
		'1_events_registered_info': 'Каждый первый объект будет иметь свое описание',
		'2_events_registered_title': 'Второе название зарегистрированного мероприятия',
		'2_events_registered_info': 'Каждый второй объект будет иметь свое описание',
		'3_events_registered_title': 'Третье название зарегистрированного мероприятия',
		'3_events_registered_info': 'Каждый третий объект будет иметь свое описание',
		'4_events_registered_title': 'Четвёртое название заригестрированного мероприятия',
		'4_events_registered_info': 'Каждый четвертый объект будет иметь свое описание',
		'5_events_registered_title': 'Пятое название зарегистрированного мероприятия',
		'5_events_registered_info': 'Каждый пятый объект будет иметь свое описание',
		'6_events_registered_title': 'Шестое название  зарегистрированного мероприятия',
		'6_events_registered_info': 'Каждый шестой объект будет иметь свое описание'
	}
	return render(request, 'events_cultural/events_registered.html', context)


def index(request):
	return render(request, 'events_cultural/index.html')
