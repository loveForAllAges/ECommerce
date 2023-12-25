from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from PIL import Image

from config.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ManyToManyField('self', symmetrical=False, related_name='children', blank=True)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", kwargs={'slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True)
    # logo = models.ImageField(upload_to='brandLogos/')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)


class Size(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Size, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ManyToManyField(Brand, related_name='product_brands')
    size = models.ManyToManyField(Size, blank=True, related_name='product_sizes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=False)
    wish = models.ManyToManyField(AUTH_USER_MODEL)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='productImages/')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        size = min(img.width, img.height)
        left = (img.width - size) / 2
        top = (img.height - size) / 2
        right = (img.width + size) / 2
        bottom = (img.height + size) / 2

        img = img.crop((left, top, right, bottom))
        img.thumbnail((4096, 4096))
        img.save(self.image.path)


class SearchHistory(models.Model):
    content = models.CharField(max_length=128)

    def __str__(self):
        return self.content
