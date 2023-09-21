from django.db import models
from product.models import Product
from django.conf import settings


# class Wishlist(models.Model):
#     customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ManyToManyField(Product)
