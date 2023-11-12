from django.db import models
from category.models import Category, Brand, Size
from django.shortcuts import reverse

class Product(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ManyToManyField(Brand, related_name='brands')
    size = models.ManyToManyField(Size, blank=True, related_name='product_sizes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def in_wishlist(self):
        return 
    
    def url(self):
        return reverse("product", kwargs={
            'pk': self.pk
        })


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='productImages/')

    def __str__(self):
        return self.product.name
