from django.forms import ModelForm
from .models import Address, Order


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('city', 'address', 'zipcode')


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone')
