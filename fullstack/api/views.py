from django.http import JsonResponse
from product.models import Product
from django.core import serializers
from search.models import SearchHistory
import json
from account.models import Address
from account.serializers import AddressSerializer, UserSerializer
from rest_framework import generics, views, response, status


def products(request):
    obj = Product.objects.all()

    serialized_data = json.loads(serializers.serialize('json', obj))
    return JsonResponse(serialized_data, safe=False)


def search(request):
    query = request.GET.get('q', '')
    result = SearchHistory.objects.filter(request__icontains=query)

    data = [{'request': i.request} for i in result]
    return JsonResponse({'result': data})
