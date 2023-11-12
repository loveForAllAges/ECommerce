from rest_framework.serializers import ModelSerializer, SerializerMethodField, ListField, ImageField
from .models import Product, ProductImage
from category.serializers import SizeSerializer, BrandSerializer, CategorySerializer


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSerializer(ModelSerializer):
    images = ListField(
        child=ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True
    )
    # images = ProductImageSerializer(many=True, read_only=True)
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
    
    def create(self, validated_data):
        images = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product
