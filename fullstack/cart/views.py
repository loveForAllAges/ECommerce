from .cart import Cart
from product.models import Product
from django.shortcuts import get_object_or_404
from product.models import Size
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class CartAPIView(APIView):
    def get(self, request):
        cart = Cart(request)
        res = cart.get_cart()
        return Response(res)

    def post(self, request):
        size_id = request.data.get('size_id', '')
        product_id = request.data.get('product_id', '')
        try:
            product = Product.objects.get(id=product_id)
            size = None
            if product.size.exists():
                size = Size.objects.get(id=size_id)
            cart = Cart(request)
            cart.add(product, size)
            res = cart.get_cart()
            st = status.HTTP_200_OK
        except Exception as ex:
            print(ex)
            st = status.HTTP_400_BAD_REQUEST
            res = {'message': 'error'}

        return Response(res, status=st)

    def delete(self, request):
        size_id = request.data.get('size_id', '')
        product_id = request.data.get('product_id', '')
        action = request.data.get('action', '')
        try:
            product = Product.objects.get(id=product_id)
            size = None
            if product.size.exists():
                size = Size.objects.get(id=size_id)
            cart = Cart(request)
            cart.update(product, action, size)
            res = cart.get_cart()
            st = status.HTTP_200_OK
        except:
            st = status.HTTP_400_BAD_REQUEST
            res = {'message': 'error'}
        return Response(res, status=st)
