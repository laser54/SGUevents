from django.shortcuts import render

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

def favorites(request):
		context: dict[str, str] = {
		'name_page': 'Избранное',
		'1_favorites_title': 'Первое название избранного  мероприятия',
		'1_favorites_info': 'Информация про избранные мероприятия',
		'2_favorites_title': 'Второе название избранного  мероприятия',
		'2_favorites_info': 'Информация про избранные мероприятия',
		'3_favorites_title': 'Третье название избранного  мероприятия',
		'3_favorites_info': 'Информация про избранные мероприятия',
		'4_favorites_title': 'Четвёртое название избранного  мероприятия',
		'4_favorites_info': 'Информация про избранные мероприятия',
		'5_favorites_title': 'Пятое название избранного мероприятия',
		'5_favorites_info': 'Информация про избранные мероприятия',
		'6_favorites_title': 'Шестое название избранного  мероприятия',
		'6_favorites_info': 'Информация про избранные мероприятия'
		}
		return render(request, 'bookmarks/favorites.html', context)

def index(request):
	return render(request, 'bookmarks/index.html')
