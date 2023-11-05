from .cart import Cart
from product.models import Product
from django.shortcuts import get_object_or_404
from category.models import Size
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class CartAPIView(APIView):
    def get(self, request):
        cart = Cart(request)
        res = cart.get_cart()
        print(res)
        return Response(res)

    def post(self, request):
        size = request.data.get('size_id', '')
        product_id = request.data.get('product_id', '')

        try:
            size = get_object_or_404(Size, id=int(size))
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.add(product.pk, size.pk)
            res = cart.get_cart()
            st = status.HTTP_200_OK
        except:
            st = status.HTTP_404_NOT_FOUND
            res = {'message': 'error'}

        return Response(res, status=st)

    def put(self, request):
        size = request.data.get('size_id', '')
        product_id = request.data.get('product_id', '')
        action = request.data.get('action', '')
        try:
            size = get_object_or_404(Size, id=int(size))
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.update(product.pk, action, size.pk)
            res = cart.get_cart()
            st = status.HTTP_200_OK
        except Exception as err:
            print(err)
            st = status.HTTP_404_NOT_FOUND
            res = {'message': 'error'}
        return Response(res, status=st)
