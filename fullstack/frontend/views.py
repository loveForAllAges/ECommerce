from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, HttpResponse as HttpResponse, redirect
from django.http import Http404, HttpRequest

from config.utils import decode_user
from frontend.permissions import AnonymousUserMixin, CartNotEmptyMixin


class AccountTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/account.html'


class WishlistTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/wish_list.html'


class LoginTemplateView(AnonymousUserMixin, TemplateView):
    template_name = 'auth/login.html'


class SignupTemplateView(AnonymousUserMixin, TemplateView):
    template_name = 'auth/signup.html'


class ActivateTemplateView(AnonymousUserMixin, TemplateView):
    def get(self, request, uidb64, token):
        user = decode_user(uidb64, token)
        if user.is_active:
            raise Http404
        user.is_active = True
        user.save()

        return redirect('login')


class SettingsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/settings.html'


class PasswordResetTemplateView(AnonymousUserMixin, TemplateView):
    template_name = 'auth/password_reset.html'


class PasswordResetProcessTemplateView(AnonymousUserMixin, TemplateView):
    template_name = 'auth/password_reset_process.html'
   
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        decode_user(kwargs['uidb64'], kwargs['token'])
        return super().get(request, *args, **kwargs)


class CheckoutTemplateView(CartNotEmptyMixin, TemplateView):
    template_name = 'pages/checkout.html'


class OrderTemplateView(TemplateView):
    template_name = 'pages/order_detail.html'


from django.urls import reverse
from product.models import Brand, Size, Category, Product, ProductImage, SearchHistory
from order.models import Delivery
from random import randint, sample, randrange, choices
from django.core.files import File
import os


def fill_db(request):
    create_brands()
    create_categories()
    create_sizes()
    create_deliveries()
    create_products()
    create_search_history()

    return HttpResponse('OK')
    # categories = request.build_absolute_uri(reverse('fill_categories'))
    # brands = request.build_absolute_uri(reverse('fill_brands'))
    # sizes = request.build_absolute_uri(reverse('fill_sizes'))
    # products = request.build_absolute_uri(reverse('fill_products'))
    # deliveries = request.build_absolute_uri(reverse('fill_deliveries'))
    # search = request.build_absolute_uri(reverse('fill_search_history'))
    # return HttpResponse(
    #     f'<a href="{categories}">Создать категории</a><br>'
    #     f'<a href="{brands}">Создать бренды</a><br>'
    #     f'<a href="{sizes}">Создать размеры</a><br>'
    #     f'<a href="{products}">Создать товары</a><br>'
    #     f'<a href="{deliveries}">Создать виды доставок</a><br>'
    #     f'<a href="{search}">Создать поисковые запросы</a>'
    # )


def fill_products(request):
    back = request.build_absolute_uri(reverse('fill_db'))
    message = 'Товары уже существуют!'

    if not Product.objects.all().exists():
        message = 'Товары созданы существуют!'
        create_products()
    return HttpResponse(
        f'{message}<br><a href="{back}">Назад</a>'
    )


def fill_brands(request):
    back = request.build_absolute_uri(reverse('fill_db'))
    message = 'Бренды уже существуют!'

    if not Brand.objects.all().exists():
        message = 'Бренды созданы!'
        create_brands()
    return HttpResponse(
        f'{message}<br><a href="{back}">Назад</a>'
    )


def fill_sizes(request):
    back = request.build_absolute_uri(reverse('fill_db'))
    message = 'Размеры уже существуют!'

    if not Size.objects.all().exists():
        message = 'Размеры созданы!'
        create_sizes()
    return HttpResponse(
        f'{message}<br><a href="{back}">Назад</a>'
    )


def fill_categories(request):
    back = request.build_absolute_uri(reverse('fill_db'))
    message = 'Категории уже существуют!'

    if not Category.objects.all().exists():
        message = 'Категории созданы!'
        create_categories()
    return HttpResponse(
        f'{message}<br><a href="{back}">Назад</a>'
    )            


def fill_deliveries(request):
    back = request.build_absolute_uri(reverse('fill_db'))
    message = 'Виды доставки уже существуют!'

    if not Delivery.objects.all().exists():
        message = 'Виды доставки созданы!'
        create_deliveries()
    return HttpResponse(
        f'{message}<br><a href="{back}">Назад</a>'
    )


def fill_search_history(request):
    back = request.build_absolute_uri(reverse('fill_db'))
    message = 'Поисковые запросы уже существуют!'

    if not SearchHistory.objects.all().exists():
        message = 'Поисковые запросы созданы!'
        create_search_history()
    return HttpResponse(
        f'{message}<br><a href="{back}">Назад</a>'
    )


def create_search_history():
    all_categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()

    for i in all_categories:
        SearchHistory.objects.get_or_create(request=i.name)

    for i in brands:
        SearchHistory.objects.get_or_create(request=i.name)

    for i in products:
        SearchHistory.objects.get_or_create(request=i.name)
    

def create_deliveries():
    item_list = [
        ('Самовывоз', 'Адрес: г. Москва, ул. Главная, 1, 1', 0, '', 'pickup'),
        ('Доставка СДЭК', 'Доставка осуществляется по Москве в пределах МКАД', 500, '', 'delivery'),
        ('Доставка курьером', 'Доставка по всей России', 0, 'Наложенный платеж', 'sdek'),
    ]
    for i in item_list:
        Delivery.objects.get_or_create(name=i[0], description=i[1], price=i[2], info=i[3], slug=i[4])


def create_categories():
    name_list = [
        ('shoes', 'Обувь', (('sneackers', 'Кроссовки'), ('boots', 'Ботинки'), ('slippers', 'Тапки'))), 
        ('clothes', 'Одежда', (('tshirts', 'Футболки'), ('trousers', 'Штаны'), ('jackets', 'Куртки'))), 
        ('accessories', 'Аксессуары', (('watch', 'Часы'), ('glasses', 'Очки'), ('bags', 'Сумки'))),
    ]
    for i in name_list:
        c = Category.objects.create(slug=i[0], name=i[1])
        for j in i[2]:
            ch = Category.objects.create(slug=j[0], name=j[1])
            c.children.add(ch)


def create_sizes():
    name_list = [
        ('41', '41'), ('42', '42'), ('43', '43'),
        ('44', '44'), ('45', '45'), ('46', '46'),
        ('s', 'S'), ('m', 'M'), ('l', 'L'),
        ('xl', 'XL'), ('xxl', 'XXL'), ('xxxl', 'XXXL'),
    ]
    for i in name_list:
        Size.objects.create(name=i[1], slug=i[0])


def create_brands():
    name_list = [
        ('Adidas', 'adidas'), ('Nike', 'nike'), ('Puma', 'puma'),
        ('Gucci', 'gucci'), ('Converse', 'converse'), ('Vans', 'vans'),
    ]
    for i in name_list:
        Brand.objects.create(name=i[0], slug=i[1])


def create_products():
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    subcategories = Category.objects.filter(parent__isnull=False)

    max_brands = len(brands)
    max_sizes = len(sizes)
    
    for i in range(1, 10):
        random_category = choices(subcategories)
        random_brands = sample(list(brands), randint(1, max_brands))
        random_sizes = sample(list(sizes), randint(1, max_sizes))

        p1 = Product.objects.create(
            name=f'product name {i}', 
            category=random_category[0], 
            description=f'this is product descriptions you can see this is product descriptions you can see this is product descriptions you can see - {i}', 
            price=randrange(1000, 1000000, 1000)
        )
        p1.brand.set(random_brands)
        p1.size.set(random_sizes)

        img_path = 'static/images/exampleProduct/1.jpeg'
        image_filename = os.path.basename(img_path)
        with open(img_path, 'rb') as img_file:
            product_image = ProductImage(product=p1, image=File(img_file, name=image_filename))
            product_image.save()
        img_path = 'static/images/exampleProduct/2.jpeg'
        image_filename = os.path.basename(img_path)
        with open(img_path, 'rb') as img_file:
            product_image = ProductImage(product=p1, image=File(img_file, name=image_filename))
            product_image.save()
        img_path = 'static/images/exampleProduct/3.jpeg'
        image_filename = os.path.basename(img_path)
        with open(img_path, 'rb') as img_file:
            product_image = ProductImage(product=p1, image=File(img_file, name=image_filename))
            product_image.save()