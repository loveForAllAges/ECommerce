from django.db import models
from django.conf import settings
from product.models import Product
from datetime import datetime
from category.models import Size
import uuid
from django.core.validators import MinValueValidator

class Delivery(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    is_pickup = models.BooleanField(default=False)
    price = models.CharField(max_length=64)


ORDER_CHOICES = (
    (0, 'Новый'), (1, 'В обработке'),  (2, 'Отправлен'), 
    (3, 'Ожидает получения'), (4, 'Завершен'), (5, 'Отменен')
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(unique=True, validators=[MinValueValidator(1001)])
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(blank=True)
    phone = models.PositiveIntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=32)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    delivery_type = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ORDER_CHOICES, default=0)
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
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.IntegerField()

    @property
    def get_total_price(self):
        return self.product.price * self.quantity
