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
    # delivery = DeliverySerializer(read_only=True)
    goods = OrderItemSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='order-detail', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('url', 'number', 'status', 'goods', 'total_price')

    def get_status(self, obj):
        return {'id': obj.status, 'name': obj.get_status_display()}
