from django.forms import ModelForm
from .models import Product, Category, Brand, ProductPhoto


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')


class ProductPhotoForm(ModelForm):
    class Meta:
        model = ProductPhoto
        fields = ('photo',)


# class SizeForm(ModelForm):
#     class Meta:
#         model = Size
#         fields = ('__all__')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ('__all__')
