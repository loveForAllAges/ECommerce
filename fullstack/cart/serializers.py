from rest_framework.serializers import ModelSerializer
from .models import Cart, CartItem
from product.serializers import ProductSerializer
from category.serializers import SizeSerializer


class CartItemSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    size = SizeSerializer(many=False, read_only=True) 
    class Meta:
        model = CartItem
        fields = ('size', 'quantity', 'total_price', 'product')


class CartSerializer(ModelSerializer):
    goods = CartItemSerializer(many=True, read_only=True, source='cartitem_set')
    class Meta:
        model = Cart
        fields = ('total_price', 'size', 'goods',)

