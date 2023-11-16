from django.http import JsonResponse

from product.models import Product
from product.serializers import ProductSerializer

from django.core import serializers
from search.models import SearchHistory
import json
from account.models import Address

from rest_framework import response, views, status, permissions, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from order.models import OrderItem, Delivery
from cart.cart import Cart

from order.serializers import DeliverySerializer, OrderSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class WishlistAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            product_id = data.get('product_id')
            product = Product.objects.get(id=product_id)
            if request.user.wishlist.filter(id=product_id).exists():
                request.user.wishlist.remove(product)
            else:
                self.request.user.wishlist.add(product)
            serializer = ProductSerializer(product, context={'request': self.request})
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return response.Response({'message': 'Ошибка'}, status=status.HTTP_400_BAD_REQUEST)


def products(request):
    obj = Product.objects.all()

    serialized_data = json.loads(serializers.serialize('json', obj))
    return JsonResponse(serialized_data, safe=False)


def search(request):
    query = request.GET.get('q', '')
    result = SearchHistory.objects.filter(request__icontains=query)

    data = [{'request': i.request} for i in result]
    return JsonResponse({'result': data})


class DeliveryListAPIView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer



class CartExists(permissions.BasePermission):
    def has_permission(self, request, view):
        cart = Cart(request)
        if len(cart):
            return True
        return False


class OrderAPIView(views.APIView):
    permission_classes = [CartExists]

    def post(self, request):
        data = request.data.copy()
        if data['delivery'] != 'pickup' and not (data['address'] and data['zip_code'] and data['city']):
            return response.Response({'message': 'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)
        
        if data['delivery'] == 'pickup':
            data['city'] = ''
            data['address'] = ''
            data['zip_code'] = ''

        if self.request.user.is_authenticated:
            data['first_name'] = self.request.user.first_name
            data['last_name'] = self.request.user.last_name
            data['email'] = self.request.user.email
            data['phone'] = self.request.user.phone
            data['customer'] = self.request.user.pk

            if data['delivery'] != 'pickup':
                address, created = Address.objects.get_or_create(customer=request.user)
                address.city = data['city']
                address.address = data['address']
                address.zip_code = data['zip_code']
                address.save()
        data['delivery'] = str(Delivery.objects.get(slug=data['delivery']).pk)
        
        order_serializer = OrderSerializer(data=data, context={'request': self.request})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        cart = Cart(request)

        for i in cart.get_cart()['goods']:
            OrderItem.objects.create(
                order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                price=i['total_price'], size_id=i['size']['id']
            )

        cart.clear()

        message = 'Заказ оформлен. На почту отправлено дублирующее письмо.'
        return response.Response({'data': order_serializer.data, 'message': message}, status=status.HTTP_200_OK)


# class ProductViewset(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    # filterset_fields = ['name']
    orderding_fields = ['id', 'price']
    search_fields = ['id', 'name', 'description']


# class ProductAPIView(views.APIView):
#     queryset = Product.objects.all()

#     def get(self, request):
#         return response.Response('')

    # def post(self, request):
    #     print('OK'*10)
    #     print(request.data)
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # serializer.save()
    #     return response.Response(serializer.data)
    #     return response.Response('OK')
