# from django import forms
# from django_select2.forms import ModelSelect2MultipleWidget
# from events_available.models import Events_online, Events_offline
# from users.models import Department


# class EventsOnlineForm(forms.ModelForm):
#     secret = forms.ModelMultipleChoiceField(
#         queryset=Department.objects.all(),  # Проверяем, что все отделы доступны для выбора
#         widget=ModelSelect2MultipleWidget(
#             model=Department,
#             search_fields=['department_name__icontains'],  # Поиск по названию отдела
#             attrs={'class': 'form-control django-select2'}
#         ),
#         required=False,
#         label="Ключ для мероприятия"
#     )

#     class Meta:
#         model = Events_online
#         fields = '__all__'
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'slug': forms.TextInput(attrs={'class': 'form-control'}),
#             'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'time_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
#             'time_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'speakers': forms.TextInput(attrs={'class': 'form-control'}),
#             'member': forms.TextInput(attrs={'class': 'form-control'}),
#             'tags': forms.TextInput(attrs={'class': 'form-control'}),
#             'platform': forms.TextInput(attrs={'class': 'form-control'}),
#             'link': forms.URLInput(attrs={'class': 'form-control'}),
#             'qr': forms.FileInput(attrs={'class': 'form-control'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#             'events_admin': forms.TextInput(attrs={'class': 'form-control'}),
#             'documents': forms.FileInput(attrs={'class': 'form-control'}),
#         }

# class EventsOfflineForm(forms.ModelForm):

#     class Meta:
#         model = Events_offline
#         fields = '__all__'
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'slug': forms.TextInput(attrs={'class': 'form-control'}),
#             'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'time_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
#             'time_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'speakers': forms.TextInput(attrs={'class': 'form-control'}),
#             'member': forms.TextInput(attrs={'class': 'form-control'}),
#             'tags': forms.TextInput(attrs={'class': 'form-control'}),
#             'town': forms.TextInput(attrs={'class': 'form-control'}),
#             'street': forms.TextInput(attrs={'class': 'form-control'}),
#             'cabinet': forms.TextInput(attrs={'class': 'form-control'}),
#             'link': forms.URLInput(attrs={'class': 'form-control'}),
#             'qr': forms.FileInput(attrs={'class': 'form-control'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#             'events_admin': forms.TextInput(attrs={'class': 'form-control'}),
#             'documents': forms.FileInput(attrs={'class': 'form-control'}),
#             'secret': ModelSelect2MultipleWidget(
#                 queryset=Department.objects.all(),
#                 search_fields=['department_name__icontains'],
#                 attrs={'class': 'form-control'}),
#         }
