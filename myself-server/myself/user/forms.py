import uuid
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from user.models import User, EmailVerification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form__input', 'placeholder': 'Введите имя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form__input', 'placeholder': 'Введите ваш пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form__input', 'placeholder': 'Введите ваше имя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form__input', 'placeholder': 'Введите ваш пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form__input', 'placeholder': 'подтвердите пароль'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form__input', 'placeholder': 'Введите ваш e-mail'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form__input', 'placeholder': 'Номер телефона'
    }))

    def save(self, commit=True):
        user = super(UserRegForm, self).save(commit=True)
        expiration = now() + timedelta(hours=4)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user

    class Meta:
        model = User
        fields = ('username', 'email',  'phone_number', 'password1', 'password2',)
