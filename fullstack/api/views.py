from product.models import Product, Brand, Size
from product.serializers import ProductSerializer, MainCategorySerializer
from category.models import Category
from category.serializers import BrandSerializer, SizeSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from product.models import SearchHistory
from account.models import Address
from account.serializers import AccountSerializer

from rest_framework import response, views, status, generics, viewsets, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from order.models import OrderItem, Delivery, Order
from cart.cart import Cart
from order.serializers import DeliverySerializer, OrderSerializer
from .filters import ProductFilter
from .serializer import SearchHistorySerializer
from config.permissions import IsStaffOrReadOnly, IsAuthenticatedOrCreateOnly, CartExists


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


class AccountAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = AccountSerializer(request.user, context={'request': request})
        print(serializer.data)
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
        data['delivery'] = str(Delivery.objects.get(slug=data['delivery']).pk)
        
        order_serializer = OrderSerializer(data=data, context={'request': self.request})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        cart = Cart(request)

        for i in cart.get_cart()['goods']:
            item = OrderItem.objects.create(
                order=order, product_id=i['product']['id'], quantity=i['quantity'], 
                price=i['total_price']
            )
            if i['size']:
                item.size_id = i['size']['id']

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
    queryset = Product.objects.all().distinct()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering_fields = ['id', 'price']
    search_fields = ['id', 'name', 'description']
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request, *args, **kwargs):
        query_list = self._get_query_list(request)
        # filter_data = self._get_filter_data()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'items': serializer.data, 'queries': query_list})

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


class HomeAPIView(views.APIView):
    def get(self, request):
        res = list()
        cats = Category.objects.filter(parent__isnull=False)

        data = Product.objects.all().order_by('-id')[:4]
        res.append({'title': 'Новинки', 'url': '?sort=-id', 'content': ProductSerializer(data, many=True, context={'request': request}).data})

        for cat in cats:
            data = Product.objects.filter(category=cat)[:4]
            res.append({'title': cat.name, 'url': f'?category={cat.id}', 'content': ProductSerializer(data, many=True, context={'request': request}).data})

        return response.Response(res, status=status.HTTP_200_OK)
    