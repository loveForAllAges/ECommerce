from django.db.models import Prefetch

from product.models import Product
from .serializers import CartSerializer, Cart, CartItem
from product.utils import product_in_wishlist_query


def get_cart(request):
    if request.user.is_authenticated:
        kwargs = {'user': request.user}
    else:
        if not request.session.session_key:
            request.session.save()
        kwargs = {'session': request.session.session_key}
    data, created = Cart.objects.prefetch_related(
        Prefetch('items', queryset=CartItem.objects.prefetch_related('size', 
            Prefetch('product', queryset=Product.objects.prefetch_related(
                'images'
            ).annotate(in_wishlist=product_in_wishlist_query(request)))
        ))
    ).get_or_create(**kwargs)
    return data


def get_serialized_cart(request):
    data = get_cart(request)
    serializer = CartSerializer(data, context={'request': request})
    return serializer.data
