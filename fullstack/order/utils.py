from .serializers import DeliverySerializer, Delivery


def get_deliveries():
    queryset = Delivery.objects.all()
    serializer = DeliverySerializer(queryset, many=True)
    return serializer.data
