from rest_framework import serializers
from .models import Delivery, Order, OrderItem
from product.serializers import ProductDetailSerializer, PreviewProductSerializer
from .validators import validate_phone
from account.models import Address


DEFAULT_ERROR_MESSAGES = {
    'blank': 'Это обязательное поле',
    'invalid': 'Неверный формат',
}


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('__all__')


class OrderItemSerializer(serializers.ModelSerializer):
    product = PreviewProductSerializer(read_only=True)
    # size = SizeSerializer(read_only=True)
    # price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('size', 'quantity', 'product', 'price')


class CheckoutSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order_detail', read_only=True)
    delivery = serializers.CharField(write_only=True)
    goods = OrderItemSerializer(many=True, read_only=True)
    first_name = serializers.CharField(
        required=False,
        max_length=128,
    )
    last_name = serializers.CharField(
        required=False,
        max_length=128,
    )
    phone = serializers.IntegerField(
        required=False,
        error_messages={
            'invalid': DEFAULT_ERROR_MESSAGES['invalid']
        }
    )
    email = serializers.EmailField(
        required=False,
        max_length=254, 
        error_messages={
            'invalid': DEFAULT_ERROR_MESSAGES['invalid']
        }
    )

    class Meta:
        model = Order
        fields = (
            'url', 'number', 'status', 'goods', 'total_price', 'delivery', 
            'customer', 'first_name', 'last_name', 'email', 'phone', 'city', 
            'zipcode', 'address'
        )

    def validate(self, attrs):
        error_dict = dict()
        print('attrs', attrs, '\n\n\n')

        if attrs.get('delivery') != 'pickup':
            if not attrs.get('city'):
                error_dict.update({'city': DEFAULT_ERROR_MESSAGES['blank']})
            if not attrs.get('zipcode'):
                error_dict.update({'zipcode': DEFAULT_ERROR_MESSAGES['blank']})
            if not attrs.get('address'):
                error_dict.update({'address': DEFAULT_ERROR_MESSAGES['blank']})
 
        user = self.context.get('request').user
        if user.is_anonymous:
            if not attrs.get('first_name'):
                error_dict.update({'first_name': DEFAULT_ERROR_MESSAGES['blank']})
            if not attrs.get('last_name'):
                error_dict.update({'last_name': DEFAULT_ERROR_MESSAGES['blank']})
            if not attrs.get('email'):
                error_dict.update({'email': DEFAULT_ERROR_MESSAGES['blank']})
            if not attrs.get('phone'):
                error_dict.update({'phone': DEFAULT_ERROR_MESSAGES['blank']})
            elif not validate_phone(attrs.get('phone')):
                error_dict.update({'phone': DEFAULT_ERROR_MESSAGES['invalid']}) 

        if error_dict:
            raise serializers.ValidationError(error_dict)
        return super().validate(attrs)

    def create(self, validated_data):
        print('validated_data', validated_data, '\n\n\n')

        user = self.context.get('request').user
        delivery = validated_data.get('delivery')
        
        try:
            params = {'delivery': Delivery.objects.get(slug=delivery)}
        except:
            raise serializers.ValidationError('Выбранный вариант доставки не найден')

        if delivery != 'pickup':
            params.update({
                'city': validated_data.get('city'),
                'zipcode': validated_data.get('zipcode'),
                'address': validated_data.get('address'),
            })

        if user.is_authenticated:
            if delivery != 'pickup':
                address, created = Address.objects.get_or_create(customer=user)
                address.city = validated_data.get('city')
                address.address = validated_data.get('address')
                address.zip_code = validated_data.get('zipcode')
                address.save()
            
            params['customer'] = user
            params.update({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
            })
        else:
            params.update({
                'first_name': validated_data.get('first_name'),
                'last_name': validated_data.get('last_name'),
                'email': validated_data.get('email'),
                'phone': validated_data.get('phone'),
            })
        
        order = Order.objects.create(**params)

        for i in validated_data.get('cart')['goods']:
            item = OrderItem.objects.create(
                order=order, 
                product_id=i['product']['id'], 
                quantity=i['quantity'], 
                price=i['total_price']
            )
            if i['size']:
                item.size_id = i['size']['id']
                item.save()

        return order


class OrderSerializer(serializers.ModelSerializer):
    goods = OrderItemSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='order_detail', read_only=True)
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
