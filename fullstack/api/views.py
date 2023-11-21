from django.http import JsonResponse

from product.models import Product, Brand, Size
from product.serializers import ProductSerializer
from category.models import Category
from category.serializers import BrandSerializer, SizeSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from django.core import serializers
from search.models import SearchHistory
import json
from account.models import Address

from rest_framework import response, views, status, permissions, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from order.models import OrderItem, Delivery
from cart.cart import Cart
from order.serializers import DeliverySerializer, OrderSerializer
from .filters import ProductFitler


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


class ProductFiltersAPIView(views.APIView):
    def get(self, request):
        brands = Brand.objects.all()
        brand_serializer = BrandSerializer(brands, many=True)
        sizes = Size.objects.all()
        size_serializer = SizeSerializer(sizes, many=True)
        caterogies = Category.objects.filter(parent__isnull=False)
        category_serializer = CategorySerializer(caterogies, many=True)
        return response.Response({
            'brands': brand_serializer.data, 'sizes': size_serializer.data, 'categories': category_serializer.data
        })


class MainCategoriesAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class SubCategoriesAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=False)
    serializer_class = CategorySerializer


class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().distinct()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ProductFitler
    orderding_fields = ['id', 'price']
    search_fields = ['id', 'name', 'description']

    def list(self, request, *args, **kwargs):
        query_list = self._get_query_list(request)
        # filter_data = self._get_filter_data()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'items': serializer.data, 'queries': query_list})

    def create(self, request, *args, **kwargs):
        print(self.serializer_class())
        return super().create(request, *args, **kwargs)

    def _get_query_list(self, request):
        query_list = list()
        search_param = request.query_params.get('search', '')
        category_param = request.query_params.get('category', '')
        brand_param = request.query_params.get('brand', '')
        size_param = request.query_params.get('size', '')

        query_list += [['search', search_param, search_param]]

        if category_param:
            lst = category_param.split(',')
            query_list += [['category', i, get_object_or_404(Category, pk=i).name] for i in lst]
        
        if brand_param:
            lst = brand_param.split(',')
            query_list += [['brand', i, get_object_or_404(Brand, pk=i).name] for i in lst]

        if size_param:
            lst = size_param.split(',')
            query_list += [['size', i, get_object_or_404(Size, pk=i).name] for i in lst]

        return query_list


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
