from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, HttpResponse
from django.contrib import admin
from django.views.generic import TemplateView


def fill_db(request):
    from category.models import Category, Size, Brand, Color
    from PIL import Image
    from django.core.files import File
    import os
    from product.models import Product, ProductImage


    def create_brands():
        name_list = [
            ('Adidas', 'adidas'), ('Nike', 'nike'), ('Puma', 'puma'),
            ('Gucci', 'gucci'), ('Converse', 'converse'), ('Vans', 'vans'),
        ]
        for i in name_list:
            Brand.objects.create(name=i[0], slug=i[1])

    def create_colors():
        name_list = [
            ('red', 'red-500', 'Красный'), ('pink', 'pink-500', 'Розовый'), ('rose', 'rose-800', 'Бордовый'),
            ('blue', 'blue-500', 'Синий'), ('sky', 'sky-500', 'Голубой'), ('dark-blue', 'blue-800', 'Темно-синий'),
            ('green', 'green-500', 'Зеленый'), ('light-green', 'emerald-400', 'Светло-зеленый'), ('dark-green', 'emerald-800', 'Темно-зеленый'),
            ('yellow', 'yellow-500', 'Желтый'), ('brown', 'amber-800', 'Коричневый'), ('orange', 'orange-500', 'Оранжевый'),
            ('violet', 'indigo-500', 'Фиолетовый'), ('white', 'white', 'Белый'), ('black', 'black', 'Черный'),
            ('gray', 'gray-500', 'Серый'),
        ]
        for i in name_list:
            Color.objects.create(slug=i[0], css=i[1], name=i[2])

    def create_categories():
        name_list = [
            ('shoes', 'Обувь'), ('clothes', 'Одежда'), ('accessories', 'Аксессуары'),
        ]
        for i in name_list:
            Category.objects.create(name=i[1], slug=i[0])

    def create_subcategories(categories):
        name_list = [
            ('sneackers', 'Кроссовки', 'shoes'), ('boots', 'Ботинки', 'shoes'), ('slippers', 'Тапки', 'shoes'),
            ('tshirts', 'Футболки', 'clothes'), ('trousers', 'Штаны', 'clothes'), ('jackets', 'Куртки', 'clothes'),
            ('watch', 'Часы', 'accessories'), ('glasses', 'Очки', 'accessories'), ('bags', 'Сумки', 'accessories'),
        ]
        for i in name_list:
            parent_cat = categories.get(slug=i[2])
            new_cat = Category.objects.create(name=i[1], slug=i[0])
            parent_cat.children.add(new_cat)

    def create_sizers(categories):
        name_list = [
            ('41', '41'), ('42', '42'), ('43', '43'),
            ('44', '44'), ('45', '45'), ('46', '46'),
            ('s', 'S'), ('m', 'M'), ('l', 'L'),
            ('xl', 'XL'), ('xxl', 'XXL'), ('xxxl', 'XXXL'),
        ]
        for i in name_list:
            Size.objects.create(name=i[1], slug=i[0])

    def create_products(brands, sizes, colors, subcategories):
        from random import randint, sample, randrange, choices
        max_brands = len(brands)
        max_colors = len(colors)
        max_sizes = len(sizes)
        
        for i in range(1, 10):
            random_category = choices(subcategories)
            random_brands = sample(list(brands), randint(1, max_brands))
            random_sizes = sample(list(sizes), randint(1, max_sizes))
            random_colors = sample(list(colors), randint(1, max_colors))

            p1 = Product.objects.create(
                name=f'product name {i}', 
                category=random_category[0], 
                description=f'this is product descriptions you can see this is product descriptions you can see this is product descriptions you can see - {i}', 
                price=randrange(1000, 1000000, 1000)
            )
            p1.brand.set(random_brands)
            p1.color.set(random_colors)
            p1.size.set(random_sizes)

            img_path = 'static/images/exampleProduct/1.jpeg'
            image_filename = os.path.basename(img_path)
            with open(img_path, 'rb') as img_file:
                product_image = ProductImage(product=p1, image=File(img_file, name=image_filename), is_main=True)
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


    def create_search_history(all_categories, brands, colors, products):
        from product.models import SearchHistory

        for i in all_categories:
            SearchHistory.objects.get_or_create(request=i.name)

        for i in brands:
            SearchHistory.objects.get_or_create(request=i.name)

        for i in products:
            SearchHistory.objects.get_or_create(request=i.name)


    categories = Category.objects.filter(parent__isnull=True)
    all_categories = Category.objects.all()
    subcategories = Category.objects.filter(parent__isnull=False)
    brands = Brand.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()

    create_brands()
    create_colors()
    create_categories()
    create_subcategories(categories)
    create_sizers(categories)
    create_products(brands, sizes, colors, subcategories)
    products = Product.objects.all()
    create_search_history(all_categories, brands, colors, products)

    return HttpResponse("OK")


def add_delivery_types(request):
    from order.models import Delivery

    item_list = [
        ('Самовывоз', 'Адрес: г. Москва, ул. Главная, 1, 1', 0, '', 'pickup'),
        ('Доставка СДЭК', 'Доставка осуществляется по Москве в пределах МКАД', 500, '', 'delivery'),
        ('Доставка курьером', 'Доставка по всей России', 0, 'Наложенный платеж', 'sdek'),
    ]

    for i in item_list:
        Delivery.objects.get_or_create(name=i[0], description=i[1], price=i[2], info=i[3], slug=i[4])

    return HttpResponse("Success")


urlpatterns = [
    # path('a/', fill_db),
    # path('admin/', admin.site.urls),
    # path('add_delivery_types', add_delivery_types),

    path('cart/', include('cart.urls')),
    # path('category/', include('category.urls')),
    path('orders/', include('order.urls')),
    path('account/', include('account.urls')),
    path('products/', include('product.urls')),
    path('adm/', include('adm.urls')),
    path('api/', include('api.urls')),
    path('chat/', include('chat.urls')),
    
    path('catalog', TemplateView.as_view(template_name='pages/catalog.html'), name='catalog'),
    # Home page view
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)