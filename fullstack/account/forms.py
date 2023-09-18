from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = settings.AUTH_USER_MODEL
        fields = UserCreationForm.Meta.fields


# class UserForm(ModelForm):
    # class Meta:
        # model = settings.AUTH_USER_MODEL
        # fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
