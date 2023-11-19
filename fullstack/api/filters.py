from django_filters.rest_framework import (
    FilterSet, BaseInFilter, CharFilter, RangeFilter
)
from product.models import Product
from django.db.models import Q


class CharFieldInFilter(BaseInFilter, CharFilter):
    pass


class ProductFitler(FilterSet):
    category = CharFieldInFilter(method='filter_category')
    brand = CharFieldInFilter(field_name='brand__id', lookup_expr='in')
    size = CharFieldInFilter(field_name='size__id', lookup_expr='in')
    price = RangeFilter()

    def filter_category(self, queryset, name, values):
        return queryset.filter(Q(category__id__in=values) | Q(category__parent__id__in=values))

    class Meta:
        model = Product
        fields = ('category', 'brand', 'size', 'price')
