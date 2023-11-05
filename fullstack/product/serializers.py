from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, ProductImage


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'is_main')


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')
    in_wishlist = SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'in_wishlist', 'images', 'url', 'price')

    def get_in_wishlist(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            res = request.user.wishlist.filter(id=obj.id).exists()
        else:
            res = False
        return res
