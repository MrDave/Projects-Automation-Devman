from .models import Student, DevmanUser
from django.forms import ModelForm, TextInput,Select, DateTimeInput, Textarea


class DevmanUserForm(ModelForm):
    class Meta:
        model = DevmanUser
        fields = ['first_name', 'telegram_id', 'email']

        widgets = {
            "first_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ФИО'
            }),
            "telegram_id": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телеграмм ID'
            }),
             "email": TextInput(attrs={
                'class': 'form-control'
            }),


        }