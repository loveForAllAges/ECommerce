from django.db import models
from django.conf import settings
from product.models import Product
from datetime import datetime


class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def get_number_of_items_in_cart(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total
    
    @property
    def get_total_price(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total_price for item in cartitems])
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def get_total_price(self):
        return self.product.price * self.quantity
