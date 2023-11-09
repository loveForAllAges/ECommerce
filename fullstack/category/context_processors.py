from .models import Category


def categories(request):
    result = list()
    category_list = Category.objects.filter(parent=None)
    
    for category in category_list:
        cat_data = {'name': category.name, 'slug': category.slug, 'logo': ''}
        child_category_list = category.children.all()

        for child_category in child_category_list:
            last_product = child_category.products.order_by('-id').first()
            if last_product:
                cat_data['logo'] = last_product.images.first().image.url
                break

        if not cat_data['logo']:
            cat_data['logo'] = 'static/images/emptyCategoryLogo.jpg'
        
        result.append(cat_data)

    return {'categories': result}
