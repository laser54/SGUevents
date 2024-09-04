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
    event = forms.ModelChoiceField(queryset=Events_online.objects.none(), label='Мероприятие')
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')

    def __init__(self, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = Events_online.objects.all()  # Задаем пустой набор по умолчанию

    def set_event_queryset(self, event_type):
        if event_type == 'online':
            self.fields['event'].queryset = Events_online.objects.all()
        elif event_type == 'offline':
            self.fields['event'].queryset = Events_offline.objects.all()
        elif event_type == 'attractions':
            self.fields['event'].queryset = Attractions.objects.all()
        elif event_type == 'for_visiting':
            self.fields['event'].queryset = Events_for_visiting.objects.all()
