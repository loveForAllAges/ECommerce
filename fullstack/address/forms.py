from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    city = forms.CharField(
        max_length=128, 
        widget=forms.TextInput(
            attrs={
                'placeholder': ' ',
                'id': 'address_city',
                'class': 'block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            }
        ),
    )
    address = forms.CharField(
        label='Адрес', max_length=128, widget=forms.TextInput(
            attrs={
                'placeholder': ' ',
                'id': 'address_address',
                'class': 'block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            }
        )
    )

    class Meta:
        model = Address
        fields = ('city', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        self.fields['address'].required = True
