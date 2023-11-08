from django.forms import ModelForm
from .models import Category, Brand


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ('__all__')
