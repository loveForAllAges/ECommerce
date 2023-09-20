from django.conf import settings
from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def create(self, item, quantity):
        item_id = str(item.id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id] = {'quantity': quantity}
        self.save()

    def update(self, item, quantity):
        item_id = str(item.id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] = quantity
        self.save()

    def get_total_price(self):
        price = 0

        print('CART VALUES', self.cart.values())
        for item in self.cart.values():
            print(item)
            item = Product.objects.get(id=item)
            price += item['quantity']

        return price

    def delete(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
