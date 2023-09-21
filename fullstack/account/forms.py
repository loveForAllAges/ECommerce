from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, UserChangeForm, AuthenticationForm
from django.core.validators import validate_email


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Введите имя', max_length=128)
    last_name = forms.CharField(label='Введите фамилию', max_length=128)
    email = forms.EmailField(max_length=255, error_messages={'invalid': 'Неверный формат!'})
    phone = forms.CharField(max_length=10)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 10:
            raise forms.ValidationError("Неверный номер телефона!")
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
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Фамилия'})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Номер телефона'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Почта', 'name': 'email', 'id': 'id_email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Повторите пароль'})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=255,
        error_messages={'invalid': 'Неверный формат!'},
        widget=forms.EmailInput(
            attrs=
            {
                "autofocus": True,
                'placeholder': 'Почта',
            }
            ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={
            "autocomplete": "current-password",
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'login-pwd',
        }
    ))

    error_messages = {
        "invalid_login": (
            "Неверная почта или пароль!"
        ),
        "inactive": ("Аккаунт не активирован!"),
    }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'phone', 'last_name')


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
