from django import forms
from events_available.models import Events_online, Events_offline
from events_cultural.models import Attractions, Events_for_visiting


class SendMessageForm(forms.Form):
    event_choices = [
        ('online', 'Онлайн мероприятия'),
        ('offline', 'Оффлайн мероприятия'),
        ('attractions', 'Достопримечательности'),
        ('for_visiting', 'Доступные для посещения'),
    ]

    event_type = forms.ChoiceField(choices=event_choices, label='Тип мероприятия')
    event = forms.ModelChoiceField(queryset=Events_online.objects.none(), label='Мероприятие', required=False)
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')

    def __init__(self, *args, **kwargs):
        event_type = kwargs.pop('event_type', None)  # Извлекаем event_type из kwargs
        super(SendMessageForm, self).__init__(*args, **kwargs)

        if event_type:
            # Устанавливаем queryset в зависимости от выбранного типа мероприятия
            self.set_event_queryset(event_type)
        else:
            # По умолчанию оставляем queryset пустым
            self.fields['event'].queryset = Events_online.objects.none()

    def set_event_queryset(self, event_type):
        if event_type == 'online':
            self.fields['event'].queryset = Events_online.objects.all()
        elif event_type == 'offline':
            self.fields['event'].queryset = Events_offline.objects.all()
        elif event_type == 'attractions':
            self.fields['event'].queryset = Attractions.objects.all()
        elif event_type == 'for_visiting':
            self.fields['event'].queryset = Events_for_visiting.objects.all()
