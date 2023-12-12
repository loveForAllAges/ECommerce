from django_filters.rest_framework import (
    FilterSet, BaseInFilter, CharFilter, RangeFilter, 
)
from product.models import Product
from django.db.models import Q


class CharFieldInFilter(BaseInFilter, CharFilter):
    pass


class ProductFilter(FilterSet):
    category = BaseInFilter(method='filter_category')
    brand = CharFieldInFilter(method='filter_brand')
    size = CharFieldInFilter(method='filter_size')
    price = RangeFilter()

    def filter_brand(self, queryset, name, values):
        try:
            return queryset.filter(brand__id__in=values)
        except:
            return queryset.none() 

    def filter_size(self, queryset, name, values):
        try:
            return queryset.filter(size__id__in=values)
        except:
            return queryset.none()            

    def filter_category(self, queryset, name, values):
        try:
            return queryset.filter(Q(category__id__in=values) | Q(category__parent__id__in=values))
        except:
            return queryset.none()
        
    class Meta:
        model = Product
        fields = ('category', 'brand', 'size', 'price')
