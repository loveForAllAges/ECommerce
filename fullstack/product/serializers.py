from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, ProductImage
from category.serializers import SizeSerializer, BrandSerializer, CategorySerializer


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'is_main')


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    in_wishlist = SerializerMethodField()
    brand = BrandSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('__all__')

    def get_in_wishlist(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            res = request.user.wishlist.filter(id=obj.id).exists()
        else:
            res = False
        return res
