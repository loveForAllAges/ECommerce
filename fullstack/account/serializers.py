from rest_framework import serializers
from .models import User, Address
from product.serializers import ProductSerializer


class UserSerializer(serializers.ModelSerializer):
    # wishlist = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city', 'address', 'zip_code')
