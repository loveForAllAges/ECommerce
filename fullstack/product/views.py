from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, views, viewsets

from .utils import preview_product_queryset, product_in_wishlist_query
from .serializers import *
from .pagination import CustomCursorPagination
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
    # TODO Не работает Сортировка вместе с пагинацией. Исправить
    # ordering_fields = ['-id', 'price']
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
    


class CatalogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PreviewProductSerializer
    pagination_class = CustomCursorPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    # TODO Не работает Сортировка вместе с пагинацией. Исправить
    # ordering_fields = ['-id', 'price']
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
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsStaffOrReadOnly]


class SearchListAPIView(generics.ListAPIView):
    # TODO Отображает все истории поиска
    queryset = SearchHistory.objects.filter()
    serializer_class = SearchHistorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
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

        res += CategorySerializer(categories, many=True, context={'request': request}).data
        return Response({
            'content': res,
        })


class WishAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
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
        data  = self.get_queryset()
        serializer = PreviewProductSerializer(data, many=True, context={'request': request})
        return Response({'content': serializer.data})

    def post(self, request, *args, **kwargs):
        data = self.get_object()
        data.wish.add(self.request.user)
        serializer = PreviewProductSerializer(data, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        data = self.get_object()
        data.wish.remove(self.request.user)
        serializer = PreviewProductSerializer(data, context={'request': request})
        return Response(serializer.data)
