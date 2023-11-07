from rest_framework import serializers
from .models import Delivery, Order, OrderItem
from product.serializers import ProductSerializer, SizeSerializer


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('__all__')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    # price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('size', 'quantity', 'product', 'price')


class OrderSerializer(serializers.ModelSerializer):
    # delivery = DeliverySerializer()
    # delivery = serializers.PrimaryKeyRelatedField(read_only=True)
    # customer = serializers.PrimaryKeyRelatedField(read_only=True)
    goods = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('__all__')
        # fields = ('id', 'number', 'customer_id', 'first_name', 'address',
        #           'last_name', 'email', 'phone', 'zip_code', 'city', 
        #           'delivery_id', 'status', 'created_at')
