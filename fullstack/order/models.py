from django.db import models
from django.conf import settings
from product.models import Product
from datetime import datetime


class Address(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    name = models.CharField(max_length=255)


class Order(models.Model):
    ORDER_CHOICES = ((1, 'Создан'), (2, 'Собран'), (3, 'Отправлен'), 
                     (4, 'Доставлен'), (5, 'Получен'), (6, 'Завершен'), (7, 'Отменен'), (8, 'Удален'))

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(blank=True)
    phone = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255)
    status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def number_of_items_in_cart(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_price for item in orderitems])
        return total

    def get_created_date(self):
        time_format = '%d.%m.%Y %H:%M'
        return self.created_at.strftime(time_format)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity
