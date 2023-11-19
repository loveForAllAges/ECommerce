from django_filters.rest_framework import (
    FilterSet, BaseInFilter, CharFilter, RangeFilter
)
from product.models import Product


class CharFieldInFilter(BaseInFilter, CharFilter):
    pass


class ProductFitler(FilterSet):
    category = CharFieldInFilter(field_name='category__category__id', lookup_expr='in')
    category = CharFieldInFilter(field_name='category__id', lookup_expr='in')
    brand = CharFieldInFilter(field_name='brand__id', lookup_expr='in')
    size = CharFieldInFilter(field_name='size__id', lookup_expr='in')
    price = RangeFilter()

    class Meta:
        model = Product
        fields = ('category', 'brand', 'size', 'price')
