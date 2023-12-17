from django.conf import settings
from .models import Cart as DBCart, CartItem
from .serializers import CartSerializer
from django.db.models import Q, Prefetch, Exists, OuterRef, Value, Case, When, BooleanField
from product.models import Product
from order.models import Order, OrderItem
from account.models import User
from config.utils import product_in_wishlist_query


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart

    def get_cart_from_db(self):
        user = self.request.user

        cart = DBCart.objects.prefetch_related(
            Prefetch('cartitem_set', queryset=CartItem.objects.prefetch_related(
                Prefetch('product', queryset=Product.objects.prefetch_related(
                    'images', 'brand', 'size'
                ).annotate(in_wishlist=product_in_wishlist_query(self.request)))
            ))
        )

        if user.is_authenticated:
            cart, created = cart.get_or_create(customer=user)
        else:
            cart, created = cart.get_or_create(session=self.session)

        return cart

    def add(self, product, size):
        cart = self.get_cart_from_db()

        query = Q(cart=cart, product=product)
        if size:
            query &= Q(size=size)
        try:
            cart_item = CartItem.objects.get(query)
            cart_item.quantity += 1
            cart_item.save()
        except:
            if size:
                CartItem.objects.create(cart=cart, product=product, size=size)
            else:
                CartItem.objects.create(cart=cart, product=product)

    def __len__(self):
        user = self.request.user
        if user.is_authenticated:
            db_crt, created = DBCart.objects.get_or_create(customer=user)
        else:
            db_crt, created = DBCart.objects.get_or_create(session=self.session.session_key)
        return db_crt.size

    def update(self, product, action, size=None):
        user = self.request.user
        try:
            is_deleted = False

            if user.is_authenticated:
                query = Q(cart__customer=user)
            else:
                query = Q(cart__session=self.session.session_key)
            query &= Q(product=product)
            if size:
                query &= Q(size=size)

            cart_item = CartItem.objects.get(query)
            
            if action == 'plus':
                cart_item.quantity += 1
            elif action == 'minus' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                is_deleted = True
            if not is_deleted:
                cart_item.save()
        except Exception as ex:
            print(ex)

    def get_cart(self):
        # cart = self.get_cart_from_db().prefetch_related('product_set__images', 'product_set_product__size', 'product_set_product__brand')
        cart = self.get_cart_from_db()
        serializer = CartSerializer(cart, context={'request': self.request})
        return serializer.data
    
    def clear(self):
        cart = self.get_cart_from_db()
        cart.delete()

    def save(self):
        self.session.modified = True
        self.session.save()
