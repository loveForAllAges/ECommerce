from django.db.models import Exists, OuterRef, Subquery
from django.contrib.auth import get_user_model

from .serializers import MainCategorySerializer, Product, Category


def product_in_wishlist_query(request):
    if request.user.is_authenticated:
        in_wishlist = Exists(Product.objects.filter(
            wish=request.user, id=OuterRef('pk')
        ))
    else:
        in_wishlist = Exists(Product.objects.none())
    return in_wishlist


def get_product_queryset(request):
    queryset = Product.objects.prefetch_related(
        'brand', 'images', 'size'
    ).annotate(
        in_wishlist=product_in_wishlist_query(request)
    )
    return queryset


def get_main_categories(request):
    data = Category.objects.filter(parent__isnull=True)
    serializer = MainCategorySerializer(data, many=True, context={'request': request})
    return serializer.data
