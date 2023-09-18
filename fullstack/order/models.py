from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    ORDER_CHOICES = ((1, 'Создан'), (2, 'Оформлен'), (3, 'Собран'), (4, 'Отправлен'), 
                     (5, 'Получен'), (6, 'Доставлен'), (7, 'Завершен'), (8, 'Отменен'))

    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
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


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity
    