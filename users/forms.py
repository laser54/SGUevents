from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'department_id', 'telegram_id']
        widgets = {
            'middle_name': forms.TextInput(attrs={'placeholder': 'Отчество (необязательно)'}),
            'department_id': forms.NumberInput(attrs={'placeholder': 'ID отдела'}),
            'telegram_id': forms.HiddenInput(),  # Указываем, что для telegram_id нужно использовать скрытый виджет
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'department_id': 'ID отдела',
        }

    def clean_department_id(self):
        department_id = self.cleaned_data.get('department_id')
        return department_id
