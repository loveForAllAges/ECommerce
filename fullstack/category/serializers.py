from rest_framework.serializers import ModelSerializer
from .models import Size, Brand, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('__all__')


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ('__all__')

