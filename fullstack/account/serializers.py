from rest_framework import serializers
from .models import User, Address
from order.serializers import OrderSerializer


class AccountSerializer(serializers.ModelSerializer):
    is_staff = serializers.SerializerMethodField()
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'is_staff', 'orders')

    def get_is_staff(self, obj):
        return obj.is_staff or obj.is_superuser


class SettingsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

    def validate_phone(self, object):
        if len(object) != 10 or not object.isdigit():
            raise serializers.ValidationError("Неверный формат номера телефона!")
        return object

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone', 'password')

    def validate_phone(self, object):
        if len(object) != 10 or not object.isdigit():
            raise serializers.ValidationError("Неверный формат номера телефона!")
        return object

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if not self.instance.check_password(attrs['old_password']):
            raise serializers.ValidationError('Введен неверный пароль')
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city', 'address', 'zip_code')


class CustomerSerializer(serializers.ModelSerializer):
    # last_address = AddressSerializer(many=True, source='address_set')
    city = serializers.CharField(source='address_set.first.city', read_only=True)
    address = serializers.CharField(source='address_set.first.address', read_only=True)
    zipcode = serializers.CharField(source='address_set.first.zipcode', read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'zipcode', 'city')
