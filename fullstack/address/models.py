from django.db import models
from django.conf import settings


class Address(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
