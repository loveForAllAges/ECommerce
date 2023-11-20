from rest_framework import serializers
from .models import Product, ProductImage
from category.serializers import SizeSerializer, BrandSerializer, CategorySerializer


class ProductImageListingField(serializers.RelatedField):
    def to_representation(self, value):
        request = self.context.get('request')
        return request.build_absolute_uri(value.image.url)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageListingField(many=True, read_only=True)
    in_wishlist = serializers.SerializerMethodField()
    # brands = BrandSerializer(many=True)
    # size = SizeSerializer(many=True, read_only=True)
    # category = CategorySerializer()
    url = serializers.HyperlinkedIdentityField(view_name='product')
    # brand = serializers.PrimaryKeyRelatedField(many=True, queryset)

    class Meta:
        model = Product
        fields = ('__all__')

    def validate(self, data):
        images_data = self.context.get('request').FILES.getlist('images')
        if not images_data or not 0 < len(images_data) <= 6:
            raise serializers.ValidationError({'images': ['Минимум 1 изображение, максимум 6.']})
        return data

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images')
        brand_data = validated_data.pop('brand', [])
        size_data = validated_data.pop('size', [])
        
        product = Product.objects.create(**validated_data)

        for brand in brand_data:
            product.brand.add(brand)

        for size in size_data:
            product.size.add(size)

        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)
        return product

    def get_in_wishlist(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            res = request.user.wishlist.filter(id=obj.id).exists()
        else:
            res = False
        return res

