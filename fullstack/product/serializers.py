from rest_framework import serializers
from .models import Product, ProductImage
from category.serializers import SizeSerializer, BrandSerializer, CategorySerializer
from category.models import Category, Brand, Size


ERROR_MESSAGES = {
    'required': 'Это обязательное поле',
    'invalid': 'Неверный формат',
    'etc': 'Неверные данные',
    'max_value': 'Максимальная цена - 10 000 000 ₽',
    'min_value': 'Минимальная цена - 1 ₽',
}


class MainCategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'url')

    def get_url(self, instance, *args, **kwargs):
        last_product = instance.products.order_by('-id').first()

        if last_product:
            url = last_product.images.first().image.url
        else:
            url = 'emptyCategoryLogo.jpg'

        request = self.context.get('request')
        return request.build_absolute_uri(url)


class ProductImageListingField(serializers.RelatedField):
    def to_representation(self, value):
        request = self.context.get('request')
        return request.build_absolute_uri(value.image.url)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageListingField(many=True, read_only=True)
    in_wishlist = serializers.BooleanField()
    # in_wishlist = serializers.SerializerMethodField()
    # size = SizeSerializer(many=True, read_only=True)
    # category = CategorySerializer()
    url = serializers.HyperlinkedIdentityField(view_name='product', lookup_field='pk', read_only=True)
    # brand = serializers.PrimaryKeyRelatedField(many=True, queryset)
    name = serializers.CharField(max_length=128, error_messages={
        'required': ERROR_MESSAGES['required'],
        'blank': ERROR_MESSAGES['required'],
        'invalid': ERROR_MESSAGES['invalid'],
        'max_length': 'Максимальная длина названия - 128 символов'
    })
    description = serializers.CharField(error_messages={
        'required': ERROR_MESSAGES['required'],
        'blank': ERROR_MESSAGES['required'],
    })
    price = serializers.IntegerField(min_value=1, max_value=10000000, error_messages={
        'required': ERROR_MESSAGES['required'],
        'invalid': ERROR_MESSAGES['invalid'],
        'max_value': ERROR_MESSAGES['max_value'],
        'min_value': ERROR_MESSAGES['min_value'],
    })
    category = serializers.PrimaryKeyRelatedField(error_messages={
        'null': ERROR_MESSAGES['required'],
        'does_not_exist': ERROR_MESSAGES['etc'],
        'required': ERROR_MESSAGES['required'],
        'incorrect_type': ERROR_MESSAGES['invalid'],
    }, queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(error_messages={
        'null': ERROR_MESSAGES['required'],
        'does_not_exist': ERROR_MESSAGES['etc'],
        'required': ERROR_MESSAGES['required'],
        'incorrect_type': ERROR_MESSAGES['invalid'],
        'empty': ERROR_MESSAGES['required']
    }, queryset=Brand.objects.all(), many=True, allow_empty=False)
    size = serializers.PrimaryKeyRelatedField(error_messages={
        'null': ERROR_MESSAGES['required'],
        'does_not_exist': ERROR_MESSAGES['etc'],
        'required': ERROR_MESSAGES['required'],
        'incorrect_type': ERROR_MESSAGES['invalid'],
    }, queryset=Size.objects.all(), required=False, many=True)

    class Meta:
        model = Product
        fields = ('__all__')

    # def validate(self, data):
        # images_data = self.context.get('request').FILES.getlist('images')
        # if not images_data or not 0 < len(images_data) <= 6:
        #     raise serializers.ValidationError({'images': ['Минимум 1 изображение, максимум 6']})
    #     return data

    # def get_in_wishlist(self, obj):
    #     request = self.context.get('request')
    #     if request.user.is_authenticated:
    #         res = request.user.wishlist.filter(id=obj.id).exists()
    #     else:
    #         res = False
    #     return res

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images')
        brand_data = validated_data.pop('brand', [])
        size_data = validated_data.pop('size', [])

        if not images_data or not 0 < len(images_data) <= 6:
            raise serializers.ValidationError({'images': ['Минимум 1 изображение, максимум 6']})
        
        product = Product.objects.create(**validated_data)

        for brand in brand_data:
            product.brand.add(brand)

        for size in size_data:
            product.size.add(size)

        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)
        return product

    def update(self, instance, validated_data):
        current_images = instance.images.all()
        images_data = self.context.get('request').FILES.getlist('images', current_images)

        if not images_data or not 0 < len(images_data) <= 6:
            raise serializers.ValidationError({'images': ['Минимум 1 изображение, максимум 6']})
        
        if images_data != current_images:
            current_images.delete()

            for image in images_data:
                ProductImage.objects.create(product=instance, image=image)

        return super().update(instance, validated_data)