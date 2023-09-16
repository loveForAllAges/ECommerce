from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.name
    

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='productsPhotos/')

    def __str__(self):
        return self.id