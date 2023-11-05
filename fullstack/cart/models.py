from django.db import models
from django.conf import settings
from product.models import Product
from category.models import Size
from datetime import datetime


class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def size(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total
    
    @property
    def total_price(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.total_price for item in cartitems])
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity
