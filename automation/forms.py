from .models import Student
from django.forms import ModelForm, TextInput,Select, DateTimeInput, Textarea


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'telegram_id', 'level']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ФИО'
            }),
            "telegram_id": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телеграмм ID'
            }),
             "level": Select(attrs={
                'class': 'form-control'
            }),


        }