from django.http import JsonResponse

from product.models import Product
from product.serializers import ProductSerializer

from django.core import serializers
from search.models import SearchHistory
import json
from account.models import Address
from account.serializers import AddressSerializer, UserSerializer
from rest_framework import generics, views, response, status


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


from rest_framework import response, views, status
from rest_framework.permissions import IsAuthenticated
from product.serializers import ProductSerializer
from account.serializers import UserSerializer
from account.models import User


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
