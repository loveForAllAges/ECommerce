from django.db.models import Exists, OuterRef

from .serializers import (
    MainCategorySerializer, Product, Category, Brand, Size, 
    FiltersBrandSerializer, FiltersSizeSerializer, FiltersCategorySerializer
)

def product_in_wishlist_query(request):
    if request.user.is_authenticated:
        in_wishlist = Exists(Product.objects.filter(
            wish=request.user, id=OuterRef('pk')
        ))
    else:
        in_wishlist = Exists(Product.objects.none())
    return in_wishlist


def preview_product_queryset(request):
    queryset = Product.objects.prefetch_related('images').annotate(
        in_wishlist=product_in_wishlist_query(request)
    )
    return queryset


def get_main_categories(request):
    # TODO Использует много запросов. ОПТИМИЗИРОВАТЬ
    data = Category.objects.filter(parent__isnull=True)
    serializer = MainCategorySerializer(data, many=True, context={'request': request})
    return serializer.data


def get_filters():
    brands = Brand.objects.all()
    brand_serializer = FiltersBrandSerializer(brands, many=True)
    sizes = Size.objects.all()
    size_serializer = FiltersSizeSerializer(sizes, many=True)
    caterogies = Category.objects.filter(parent__isnull=False)
    category_serializer = FiltersCategorySerializer(caterogies, many=True)
    return {
        'filters': {
            'brands': brand_serializer.data, 
            'sizes': size_serializer.data, 
            'categories': category_serializer.data
        }
    }
