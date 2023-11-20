from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Size, Brand, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ('__all__')


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ('__all__')

