from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, views, viewsets

from .utils import preview_product_queryset, product_in_wishlist_query
from .serializers import *
from .pagination import CustomCursorPagination, CustomPageNumberPagination
from .filters import ProductFilter
from .decorators import (
    cart_and_categories, cart_and_categories_and_filters_and_queries
)

# from config.permissions import IsStaffOrReadOnly


class MoreProductAPIView(generics.ListAPIView):
    serializer_class = PreviewProductSerializer
    pagination_class = CustomCursorPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    ordering = '-id'
    ordering_fields = ['id', 'price']
    search_fields = ['id', 'name', 'description']

    def get_queryset(self):
        queryset = preview_product_queryset(self.request).distinct()
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        next = None
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            next = self.paginator.get_paginated_response()
        return Response({'content': serializer.data, 'next': next})
    

class CatalogListAPIView(generics.ListAPIView):
    serializer_class = PreviewProductSerializer
    pagination_class = CustomCursorPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['id', 'price']
    ordering = '-id'
    search_fields = ['id', 'name', 'description']

    def get_queryset(self):
        queryset = preview_product_queryset(self.request).distinct()
        return queryset
    
    @cart_and_categories_and_filters_and_queries
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        next = None
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        next = self.paginator.get_paginated_response(request)
        return Response({'content': serializer.data, 'next': next})


class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProductDetailSerializer
    # permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related(
            'images', 'brand', 'size'
        ).annotate(in_wishlist=product_in_wishlist_query(self.request))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class SearchListAPIView(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    filter_backends = [SearchFilter]
    search_fields = ('content',)


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

        res += CategorySerializer(categories, many=True, context={'request': request}).data
        return Response({
            'content': res,
        })


class WishAPIView(views.APIView):
    serializer_class = PreviewProductSerializer

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
        response = []
        if request.user.is_authenticated:
            data  = self.get_queryset()
            serializer = PreviewProductSerializer(data, many=True, context={'request': request})
            response = serializer.data
        return Response({'content': response})

    def post(self, request, *args, **kwargs):
        response = None
        if request.user.is_authenticated:
            data = self.get_object()
            data.wish.add(self.request.user)
            serializer = PreviewProductSerializer(data, context={'request': request})
            response = serializer.data
        return Response(response)

    def delete(self, request, *args, **kwargs):
        response = None
        if request.user.is_authenticated:
            data = self.get_object()
            data.wish.remove(self.request.user)
            serializer = PreviewProductSerializer(data, context={'request': request})
            response = serializer.data
        return Response(response)
