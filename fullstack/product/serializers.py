from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product, ProductImage, Size, Brand, Category, SearchHistory


ERROR_MESSAGES = {
    'required': 'Это обязательное поле',
    'blank': 'Это обязательное поле',
    'invalid': 'Неверный формат',
    'max_value': 'Максимальная цена - 10 000 000 ₽',
    'min_value': 'Минимальная цена - 1 ₽',
    'does_not_exist': 'Неверные данные',
    'incorrect_type': 'Неверный формат',
    'null': 'Это обязательное поле',
    'empty': 'Это обязательное поле',
}


class FiltersCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class FiltersBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('__all__')


class FiltersSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('__all__')


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ('content',)


class MainCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'image')

    def get_image(self, instance, *args, **kwargs):
        child = Category.objects.filter(parent=instance).order_by('-id').first()
        last_product = child.products.order_by('-id').first()

        if last_product:
            request = self.context.get('request')
            res = request.build_absolute_uri(last_product.images.first().image.url)
        else:
            res = None

        return res


class ProductImageListingField(serializers.RelatedField):
    def to_representation(self, value):
        request = self.context.get('request')
        return request.build_absolute_uri(value.image.url)


class PreviewProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_detail')
    images = ProductImageListingField(many=True, read_only=True)
    in_wishlist = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ('id', 'url', 'name', 'price', 'images', 'in_wishlist')


class CartProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_detail')
    images = ProductImageListingField(many=True, read_only=True)
    in_wishlist = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ('id', 'url', 'name', 'price', 'images', 'in_wishlist')


class CategorySerializer(serializers.ModelSerializer):
    # title = serializers.ModelField('name')
    title = serializers.SerializerMethodField()
    products = PreviewProductSerializer(many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('url', 'title', 'products')

    def get_title(self, obj):
        return obj.name

    def get_url(self, obj):
        return reverse(
            'catalog', request=self.context.get('request')
        ) + '?category=' + str(obj.id)


class ProductBrandSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ('name', 'url')

    def get_url(self, object):
        return reverse(
            'catalog', request=self.context.get('request')
        ) + '?brand=' + str(object.id)


class ProductCategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'url')

    def get_url(self, object):
        return reverse(
            'catalog', request=self.context.get('request')
        ) + '?category=' + str(object.id)


class ProductDetailSerializer(serializers.ModelSerializer):
    in_wishlist = serializers.BooleanField()
    # category = FiltersCategorySerializer()
    brand = ProductBrandSerializer(many=True)
    category = ProductCategorySerializer()
    size = FiltersSizeSerializer(many=True)
    # brand = FiltersBrandSerializer(many=True)
    # size = FiltersSizeSerializer(many=True)
    images = ProductImageListingField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'brand', 'size', 
            'category', 'images', 'in_wishlist',
        )



class ProductCreateSerializer(serializers.ModelSerializer):
    images = ProductImageListingField(many=True, read_only=True)
    in_wishlist = serializers.BooleanField()
    # url = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk', read_only=True)
    name = serializers.CharField(
        max_length=128, 
        error_messages=ERROR_MESSAGES.update(
            {'max_length': 'Максимальная длина названия - 128 символов'}
        )
    )
    description = serializers.CharField(error_messages=ERROR_MESSAGES)
    price = serializers.IntegerField(min_value=1, max_value=10000000, error_messages=ERROR_MESSAGES)
    category = serializers.PrimaryKeyRelatedField(
        error_messages=ERROR_MESSAGES, 
        queryset=Category.objects.all(), write_only=True
    )
    brand = serializers.PrimaryKeyRelatedField(
        error_messages=ERROR_MESSAGES, 
        queryset=Brand.objects.all(), 
        many=True, allow_empty=False, write_only=True
    )
    size = serializers.PrimaryKeyRelatedField(
        error_messages=ERROR_MESSAGES, 
        queryset=Size.objects.all(), 
        required=False, many=True, write_only=True
    )

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'brand', 'size', 
            'category', 'images', 'in_wishlist',
        )

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