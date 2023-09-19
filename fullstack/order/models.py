from django.db import models
from django.conf import settings
from product.models import Product
from datetime import datetime


class Order(models.Model):
    ORDER_CHOICES = ((1, 'Создан'), (2, 'Оформлен'), (3, 'Собран'), (4, 'Отправлен'), 
                     (5, 'Получен'), (6, 'Доставлен'), (7, 'Завершен'), (8, 'Отменен'))

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(blank=True)
    phone = models.PositiveIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_CHOICES, default=1)

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


class Address(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=128)
