from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractBaseUser
from product.models import Product


class CustomUserManager(UserManager):
    def _create_user(self, first_name, last_name, phone, email, password, **extra_fields):
        if not email:
            raise ValueError("Неверная почта")
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, phone=phone, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, first_name=None, phone=None, last_name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, last_name, phone, email, password, **extra_fields)
    
    def create_superuser(self, first_name=None, phone=None, last_name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(first_name, last_name, phone, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=10)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])


class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=32)
