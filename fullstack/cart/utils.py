from django.db.models import Prefetch

from product.models import Product
from .serializers import CartSerializer, Cart, CartItem
from product.utils import product_in_wishlist_query


def params_for_cart(request):
    if request.user.is_authenticated:
        kwargs = {'user': request.user}
    else:
        if not request.session.session_key:
            request.session.save()
        kwargs = {'session': request.session.session_key}
    return kwargs


def get_cart(request):

    data, created = Cart.objects.prefetch_related(
        Prefetch('items', queryset=CartItem.objects.prefetch_related('size', 
            Prefetch('product', queryset=Product.objects.prefetch_related(
                'images'
            ).annotate(in_wishlist=product_in_wishlist_query(request)))
        ))
    ).get_or_create(**params_for_cart(request))
    return data


def remove_cart(request):
    Cart.objects.filter(**params_for_cart(request)).delete()


def cart_not_empty(request):
    res = Cart.objects.filter(**params_for_cart(request), items__isnull=False).exists()
    print(res)
    return res


def get_serialized_cart(request):
    data = get_cart(request)
    serializer = CartSerializer(data, context={'request': request})
    return serializer.data
