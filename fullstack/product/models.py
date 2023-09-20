from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


# class Size(models.Model):
#     name = models.CharField(max_length=32)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    # cover = models.ImageField(upload_to='productImages/')

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImages/')

    def __str__(self):
        return self.id