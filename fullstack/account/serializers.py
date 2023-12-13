from rest_framework import serializers
from .models import User, Address
from product.serializers import ProductSerializer
from order.serializers import OrderSerializer


# class UserSerializer(serializers.ModelSerializer):
    # wishlist = ProductSerializer(many=True, read_only=True)
    # is_adm = serializers.SerializerMethodField()

    # class Meta:
    #     model = User
    #     fields = ('__all__')

    # def get_is_adm(self, obj):
    #     print('------', obj)
    #     return ''
    

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
