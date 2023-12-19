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
        'brands': brand_serializer.data, 
        'sizes': size_serializer.data, 
        'categories': category_serializer.data
    }


def get_queries(request):
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
