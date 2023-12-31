from django.db import models
from django.conf import settings
from product.models import Product
from product.models import Size
from datetime import datetime


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='cart'
    )
    session = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def size(self):
        cartitems = self.items.all()
        total = sum([item.quantity for item in cartitems])
        return total
    
    @property
    def total_price(self):
        cartitems = self.items.all()
        total = sum([item.total_price for item in cartitems])
        return total


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='in_cart',
    )
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items',
    )
    size = models.ForeignKey(
        Size, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return self.id
