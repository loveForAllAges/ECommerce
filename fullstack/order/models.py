from django.db import models
from product.models import Product
from datetime import datetime
from category.models import Size
import uuid
from account.models import User
from django.shortcuts import reverse
from django.utils.text import slugify


class Delivery(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    price = models.IntegerField()
    info = models.CharField(max_length=32, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


ORDER_CHOICES = (
    (0, 'Создан'), (1, 'В обработке'),  (2, 'Отправлен'), 
    (3, 'Ожидает получения'), (4, 'Завершен')
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(unique=True, blank=True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(blank=True)
    phone = models.PositiveIntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ORDER_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def number_of_items_in_cart(self):
        orderitems = self.goods.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})

    @property
    def total_price(self):
        orderitems = self.goods.all()
        total = sum([item.total_price for item in orderitems])
        return total

    def get_created_date(self):
        time_format = '%d.%m.%Y %H:%M'
        return self.created_at.strftime(time_format)

    def save(self, *args, **kwargs):
        try:
            if not self.number:
                latest = Order.objects.latest('number')
                self.number = latest.number + 1
        except:
            self.number = 1001
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='goods')
    quantity = models.PositiveIntegerField(default=0)
    price = models.IntegerField()

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
