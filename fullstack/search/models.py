from django.db import models
from account.models import User


class SearchHistory(models.Model):
    request = models.CharField(max_length=128)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.request
