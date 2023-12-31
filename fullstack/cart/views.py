from django.db.models import F, Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import CartItem
from .utils import get_cart, get_serialized_cart
from product.models import Product
from product.models import Size


class CartAPIView(APIView):
    def post(self, request):
        print(request.data)
        size_id = request.data.get('size', None)
        product_id = request.data.get('product', None)
        response = {'message': 'Ошибка'}
        try:
            q = {}
            cart = get_cart(request)
            if size_id:
                q['size'] = Size.objects.get(pk=size_id)
            q.update({'product': Product.objects.get(pk=product_id, **q), 'cart': cart})
            count = CartItem.objects.filter(**q).update(quantity=F('quantity') + 1)
            if count == 0:
                CartItem.objects.create(**q)
            response.update({'message': 'Товар добавлен в корзину', 'content': get_serialized_cart(request)})
            st = status.HTTP_200_OK
        except Exception as ex:
            print(ex)
            st = status.HTTP_400_BAD_REQUEST
        return Response(response, status=st)

    def put(self, request):
        size_id = request.data.get('size', None)
        product_id = request.data.get('product', None)
        response = {'message': 'Ошибка'}
        try:
            cart = get_cart(request)
            q = Q(size=Size.objects.get(pk=size_id)) if size_id else Q(size__isnull=True)
            q &= Q(product=Product.objects.get(Q(pk=product_id) & q), cart=cart)
            item = CartItem.objects.get(Q(quantity__gt=0) & q)
            item.quantity -= 1
            item.save()
            if item.quantity == 0: item.delete()
            response.update({'message': 'Корзина обновлена', 'content': get_serialized_cart(request)})
            st = status.HTTP_200_OK
        except Exception as ex:
            print(ex)
            st = status.HTTP_400_BAD_REQUEST
        return Response(response, status=st)
