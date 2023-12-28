from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import CartProductSerializer, FiltersSizeSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    size = FiltersSizeSerializer(many=False, read_only=True) 
    class Meta:
        model = CartItem
        fields = ('size', 'quantity', 'total_price', 'product')


class CartSerializer(serializers.ModelSerializer):
    goods = CartItemSerializer(many=True, read_only=True, source='items')

    class Meta:
        model = Cart
        fields = ('size', 'total_price', 'goods')
