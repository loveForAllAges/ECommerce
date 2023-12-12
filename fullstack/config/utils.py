from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Exists, OuterRef
from django.contrib.auth import get_user_model

from product.models import Product

from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


def get_product_queryset(request):
    if request.user.is_authenticated:
        in_wishlist = Exists(get_user_model().objects.filter(
            id=request.user.id,
            wishlist=OuterRef('pk')
        ))
    else:
        in_wishlist = Exists()
    queryset = Product.objects.prefetch_related(
        'brand', 'images', 'size'
    ).annotate(
        in_wishlist=in_wishlist
    )
    return queryset
