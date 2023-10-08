from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ManyToManyField('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.slug
