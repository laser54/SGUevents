from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def application_for_admin_rights(request):
		context: dict[str, str] = {
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
		return render(request, 'application_for_admin_rights/application_for_admin_rights.html', context)