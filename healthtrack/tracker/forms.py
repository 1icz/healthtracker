from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Measurement


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['date', 'systolic', 'diastolic', 'pulse', 'note']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'systolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 120',
                'min': 50, 'max': 300,
            }),
            'diastolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 80',
                'min': 30, 'max': 200,
            }),
            'pulse': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 70',
                'min': 30, 'max': 250,
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваши ощущения или комментарий...',
            }),
        }
        labels = {
            'date': 'Дата',
            'systolic': 'Верхнее давление',
            'diastolic': 'Нижнее давление',
            'pulse': 'Пульс',
            'note': 'Заметка',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }