from django import forms
from .models import User
from django.contrib.auth.forms import (
    UserCreationForm, PasswordResetForm, 
    SetPasswordForm, UserChangeForm, 
    AuthenticationForm, PasswordChangeForm
)
from django.core.validators import validate_email


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField(error_messages={'invalid': 'Неверный формат!'})
    phone = forms.CharField(max_length=10)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 10 or not phone.isdigit():
            raise forms.ValidationError("Неверный формат номера телефона!")
        return phone

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Почта занята!')
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Неверный формат!")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Введите имя',
            "autofocus": True
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Фамилия'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Номер телефона'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Почта', 
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Повторите пароль'
        })


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=255,
        error_messages={'invalid': 'Неверный формат!'},
        widget=forms.EmailInput(
        attrs={
            "autofocus": True,
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm', 
            'placeholder': 'Введите почту',
        }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={
            "autocomplete": "current-password",
            'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm',
            'placeholder': 'Введите пароль',
        }
    ))

    error_messages = {
        "invalid_login": "Неверная почта или пароль!",
        "inactive": "Аккаунт не активирован!",
    }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
    )
    new_password1 = forms.CharField(
        label= "Новый пароль",
    )
    new_password2 = forms.CharField(
        label= "Повторите пароль",
    )
    error_messages = {
        "password_incorrect": (
            "Неверный пароль"
        ),
        "password_mismatch": (
            "Пароли не совпадают"
        ),
    }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label='Почта', max_length=255, widget=forms.EmailInput(
            attrs={
                'class': 'block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none focus:outline-none focus:ring-1 focus:ring-black focus:border-black peer disabled:cursor-not-allowed disabled:border-gray-200 disabled:text-gray-500',
                'placeholder': '',
            }
        )
    )
    phone = forms.CharField(
        label='Номер телефона', max_length=10, widget=forms.TextInput(
            attrs={
                'class': 'block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none focus:outline-none focus:ring-1 focus:ring-black focus:border-black peer disabled:cursor-not-allowed disabled:border-gray-200 disabled:text-gray-500',
                'placeholder': '',
            }
        )
    )
    first_name = forms.CharField(
        label='Имя', max_length=128, widget=forms.TextInput(
            attrs={
                'class': 'block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none focus:outline-none focus:ring-1 focus:ring-black focus:border-black peer disabled:cursor-not-allowed disabled:border-gray-200 disabled:text-gray-500',
                'placeholder': '',
            }
        )
    )
    last_name = forms.CharField(
        label='Фамилия', max_length=128, widget=forms.TextInput(
            attrs={
                'class': 'block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none focus:outline-none focus:ring-1 focus:ring-black focus:border-black peer disabled:cursor-not-allowed disabled:border-gray-200 disabled:text-gray-500',
                'placeholder': '',
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 10 or not phone.isdigit():
            raise forms.ValidationError("Неверный формат номера телефона!")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone'].required = True
        self.fields['email'].disabled = True


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=255,
        error_messages={'invalid': 'Неверный формат!'},
        widget=forms.EmailInput(
            attrs={
                'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm',
                'placeholder': 'Введите почту',
                "autocomplete": "email"
            }
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадают!",
    }

    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm',
                "autocomplete": "new-password",
                'placeholder': 'Придумайте пароль'
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={
                'class': 'mt-1 block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 text-sm',
                "autocomplete": "new-password",
                'placeholder': 'Повторите новый пароль'
            }
        ),
    )
