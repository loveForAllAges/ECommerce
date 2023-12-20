from rest_framework import serializers
from .models import Delivery, Order, OrderItem
from product.serializers import ProductDetailSerializer, PreviewProductSerializer
from django.shortcuts import get_object_or_404


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('__all__')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    # size = SizeSerializer(read_only=True)
    # price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('size', 'quantity', 'product', 'price')


class OrderSerializer(serializers.ModelSerializer):
    goods = OrderItemSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='order-detail', read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('url', 'number', 'status', 'goods', 'total_price', 'delivery', 'customer', 'first_name', 'last_name', 'email')

    def get_status(self, obj):
        return {'id': obj.status, 'name': obj.get_status_display()}
    
    # def create(self, validated_data):
    #     print(validated_data)
    #     delivery = get_object_or_404(Delivery, slug=validated_data.get('delivery'))
    #     validated_data['delivery'] = delivery
    #     return super().create(validated_data)
