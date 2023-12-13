from product.models import Product, Brand, Size, SearchHistory
from product.serializers import ProductSerializer, MainCategorySerializer

from category.models import Category
from category.serializers import BrandSerializer, SizeSerializer, CategorySerializer

from django.db.models import Exists, OuterRef, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from account.models import User

from account.models import Address
from account.serializers import AccountSerializer

from rest_framework import (
    response, views, status, generics, permissions,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from order.models import OrderItem, Delivery, Order
from order.serializers import DeliverySerializer, OrderSerializer

from cart.cart import Cart

from .filters import ProductFilter
from .serializer import SearchHistorySerializer
from .pagination import CustomCursorPagination

from config.permissions import IsStaffOrReadOnly, IsAuthenticatedOrCreateOnly, CartExists
from config.functions import send_email
from config.utils import get_product_queryset


class WishlistAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            product_id = data.get('product_id')
            product = Product.objects.annotate(
                in_wishlist=~Exists(User.objects.filter(
                    id=self.request.user.id,
                    wishlist=OuterRef('pk')
                ))
            ).get(id=product_id)
            if request.user.wishlist.filter(id=product_id).exists():
                request.user.wishlist.remove(product)
            else:
                request.user.wishlist.add(product)
            serializer = ProductSerializer(product, context={'request': self.request})
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return response.Response({'message': 'Ошибка'}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryListAPIView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class AccountAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            in_wishlist = Exists(User.objects.filter(
                id=self.request.user.id,
                wishlist=OuterRef('pk')
            ))
        else:
            in_wishlist = Exists()
        queryset = User.objects.prefetch_related(
            Prefetch('orders', queryset=Order.objects.prefetch_related(
                Prefetch('goods', queryset=OrderItem.objects.prefetch_related(
                    Prefetch('product', queryset=Product.objects.prefetch_related('images', 'brand', 'size').annotate(in_wishlist=in_wishlist))
                ))
            )),
        ).get(id=self.request.user.id)
        print(queryset.orders)
        return queryset

    def get(self, request):
        serializer = AccountSerializer(self.get_queryset(), context={'request': request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class OrderAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly, CartExists]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
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
        data['delivery'] = Delivery.objects.get(slug=data['delivery']).pk
        
        order_serializer = OrderSerializer(data=data, context={'request': self.request})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        cart = Cart(request)
        url = request.build_absolute_uri(order.url())

        for i in cart.get_cart()['goods']:
            item = OrderItem.objects.create(
                order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                price=i['total_price']
            )
            if i['size']:
                item.size_id = i['size']['id']
                item.save()

        cart.clear()

        send_email(request, request.user, 'Заказ оформлен', f'Заказ успешно оформлен! Отслеживание заказа: {url}')
        message = 'Заказ оформлен. На почту отправлено дублирующее письмо.'
        return response.Response({'url': url, 'message': message}, status=status.HTTP_200_OK)


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
    serializer_class = MainCategorySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     serializer = self.get_serializer(queryset, many=True)
    #     return response.Response(serializer.data)


class SubCategoriesAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=False)
    serializer_class = CategorySerializer


class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]


class SearchAPIListView(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['request']


class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomCursorPagination
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # filterset_class = ProductFilter
    # ordering_fields = ['id', 'price']
    # search_fields = ['id', 'name', 'description']
    # permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = get_product_queryset(self.request).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        query_list = self._get_query_list(request)
        res = {'queries': query_list}
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            assert self.paginator is not None
            res.update(self.paginator.get_paginated_response())
        else:
            serializer = self.get_serializer(queryset, many=True)
        res['items'] = serializer.data
        return response.Response(res)

    def _get_query_list(self, request):
        query_list = list()
        search_param = request.query_params.get('search', '')
        category_param = request.query_params.get('category', '')
        brand_param = request.query_params.get('brand', '')
        size_param = request.query_params.get('size', '')

        query_list += [['search', search_param, search_param]]

        brand_param = [i for i in brand_param.split(',') if i.isdigit()]
        size_param = [i for i in size_param.split(',') if i.isdigit()]
        category_param = [i for i in category_param.split(',') if i.isdigit()]
        
        if brand_param:
            query_list += [('brand', i.id, i.name) for i in Brand.objects.filter(id__in=brand_param)]
        if size_param:
            query_list += [('size', i.id, i.name) for i in Size.objects.filter(id__in=size_param)]
        if category_param:
            query_list += [('category', i.id, i.name) for i in Category.objects.filter(id__in=category_param)]

        return query_list


class HomeAPIView(views.APIView):
    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        res = list()
        cats = Category.objects.filter(parent__isnull=False)
        products = get_product_queryset(request)
        data = products.order_by('-id')[:4]
        res.append({
            'title': 'Новинки', 
            'url': '?sort=-id', 
            'content': ProductSerializer(data, many=True, context={'request': request}).data
        })

        for cat in cats:
            data = products.filter(category=cat)[:4]
            res.append({
                'title': cat.name, 
                'url': f'?category={cat.id}', 
                'content': ProductSerializer(data, many=True, context={'request': request}).data
            })

        return response.Response(res, status=status.HTTP_200_OK)
