from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    # Определение telegram_id как скрытого поля
    telegram_id = forms.CharField(widget=forms.HiddenInput(), required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'department_id', 'telegram_id']
        widgets = {
            'middle_name': forms.TextInput(attrs={'placeholder': 'Отчество (необязательно)'}),
            'department_id': forms.NumberInput(attrs={'placeholder': 'ID отдела'}),
            # Можно задать атрибуты для других полей, если это необходимо
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'department_id': 'ID отдела',
        }
        # Дополнительно можно задать help_texts, error_messages и т.д.

    # Этот метод не требуется, если вы не планируете дополнительно валидировать department_id
    # Но если вам нужна специфическая логика валидации, его стоит оставить
    def clean_department_id(self):
        department_id = self.cleaned_data.get('department_id')
        return department_id
