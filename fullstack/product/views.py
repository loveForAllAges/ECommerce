from typing import Any
from django.db import models
from .models import Product, ProductImage
from django.views.generic import DetailView
from .utils import get_product_queryset, product_in_wishlist_query
from django.db.models import Exists, OuterRef, Prefetch
from django.contrib.auth import get_user_model


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'usage/product.html'

#     def get_queryset(self):
#         queryset = get_product_queryset(self.request)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rec_list'] = Product.objects.prefetch_related('images').annotate(
#             in_wishlist=product_in_wishlist_query(self.request)
#         )[:4]
#         return context


from rest_framework import generics, response, views, status
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import *
from .pagination import CustomCursorPagination
from config.permissions import IsStaffOrReadOnly
from .decorators import cart_and_categories
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework import views, response, authentication


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


class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]


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


# class SubCategoriesAPIView(generics.ListAPIView):
#     queryset = Category.objects.filter(parent__isnull=False)
#     serializer_class = CategorySerializer


class SearchAPIListView(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['request']


class HomeAPIView(views.APIView):
    @cart_and_categories
    def get(self, request):
        products = Product.objects.prefetch_related('images').annotate(
            in_wishlist=product_in_wishlist_query(request)
        )
        categories = Category.objects.filter(
            parent__isnull=False, products__isnull=False
        ).prefetch_related(Prefetch('products', queryset=products)).distinct()

        res = [{
            'title': 'Новое', 
            'url': request.build_absolute_uri(reverse('catalog')) + '?sort=-id', 
            'products': PreviewProductSerializer(
                products.order_by('-id')[:8], 
                many=True, context={'request': request}
            ).data
        }]

        print(res)
        res += CategorySerializer(categories, many=True, context={'request': request}).data
        return response.Response({
            'content': res,
        })


class ProductWishAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PreviewProductSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(wish=self.request.user).annotate(
            in_wishlist=product_in_wishlist_query(self.request)
        ).prefetch_related('images')
        return queryset

    def get_object(self):
        queryset = Product.objects.annotate(
            in_wishlist=product_in_wishlist_query(self.request)
        ).prefetch_related('images')

        obj = get_object_or_404(queryset, pk=self.request.data.get('product_id'))
        return obj

    @cart_and_categories
    def get(self, request, *args, **kwargs):
        data  = self.get_queryset()
        serializer = PreviewProductSerializer(data, many=True, context={'request': request})
        return response.Response({'content': serializer.data})

    def post(self, request, *args, **kwargs):
        data = self.get_object()
        data.wish.add(self.request.user)
        serializer = PreviewProductSerializer(data, context={'request': request})
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        data = self.get_object()
        data.wish.remove(self.request.user)
        serializer = PreviewProductSerializer(data, context={'request': request})
        return response.Response(serializer.data)
