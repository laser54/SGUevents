from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'department_id', 'telegram_id']
        widgets = {
            'middle_name': forms.TextInput(attrs={'placeholder': 'Отчество (необязательно)'}),
            'department_id': forms.NumberInput(attrs={'placeholder': 'ID отдела'}),
            'telegram_id': forms.HiddenInput(),  # Скрытое поле для telegram_id
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'department_id': 'ID отдела',
        }

    def clean_telegram_id(self):
        telegram_id = self.cleaned_data.get('telegram_id')
        # Валидация поля telegram_id на предмет наличия значения для обычных пользователей
        if not telegram_id:
            raise forms.ValidationError("Требуется идентификатор Telegram для регистрации.")
        return telegram_id

    def clean_department_id(self):
        department_id = self.cleaned_data.get('department_id')
        if not department_id:
            raise forms.ValidationError("Требуется указать ID отдела.")
        return department_id
