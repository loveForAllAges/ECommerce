# from django import forms
# from .models import Order
# from account.models import User


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('first_name', 'last_name', 'email', 'phone', 'zip_code', 'city', 'address')


# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone']

#     def clean_phone(self):
#         phone = self.cleaned_data['phone']
#         if len(phone) != 10 or not phone.isdigit():
#             raise forms.ValidationError("Неверный формат номера телефона!")
#         return phone
