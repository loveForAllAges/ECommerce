from django.forms import ModelForm
from .models import Product, Category, Brand, ProductImage


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')


class ProductPhotoForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)
