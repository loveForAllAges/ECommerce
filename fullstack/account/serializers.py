from rest_framework import serializers
from .models import User, Address
from order.serializers import OrderSerializer


class AccountSerializer(serializers.ModelSerializer):
    is_staff = serializers.SerializerMethodField()
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'is_staff', 'orders')

    def get_is_staff(self, obj):
        return obj.is_staff or obj.is_superuser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city', 'address', 'zip_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
