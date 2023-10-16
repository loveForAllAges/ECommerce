from django.utils.text import slugify
from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ManyToManyField('self', symmetrical=False, related_name='children', blank=True)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", kwargs={
            'slug': self.slug
        })


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


class Color(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True)
    css = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Color, self).save(*args, **kwargs)


class Size(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Size, self).save(*args, **kwargs)
