from django.conf import settings
from product.models import Product
from .models import Cart as DBCart, CartItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def add(self, product):
        user = self.request.user

        if user.is_authenticated:
            db_cart, created = DBCart.objects.get_or_create(customer=user)
            try:
                cart_item = CartItem.objects.get(cart=db_cart, product=product)
                cart_item.quantity += 1
                cart_item.save()
            except:
                CartItem.objects.create(cart=db_cart, product=product, quantity=1)   
        else:
            product_id = str(product.id)

            if product_id in self.cart:
                self.cart[product_id]['quantity'] += 1
            else:
                self.cart[product_id] = {'quantity': 1}

            self.save()

    # def __iter__(self):
    #     user = self.request.user

    #     if user.is_authenticated:
    #         db_crt, created = DBCart.objects.get_or_create(customer=user)
    #         products = db_crt.cartitem_set.all()
    #         for item in products:
    #             yield item
    #     else:
    #         product_ids = self.cart.keys()
    #         cart = self.cart.copy()

    #         products = Product.objects.filter(id__in=product_ids)
            
    #         for product in products:
    #             cart[str(product.id)]['product'] = product
    #             cart[str(product.id)]['price'] = product.price

    #         for item in cart.values():
    #             item['get_total_price'] = item['price'] * item['quantity']
    #             yield item

    def __len__(self):
        user = self.request.user
        
        if user.is_authenticated:
            db_crt, created = DBCart.objects.get_or_create(customer=user)
            return db_crt.get_number_of_items_in_cart
        else:
            return sum([item['quantity'] for item in self.cart.values()])

    def update(self, product, action):
        user = self.request.user

        if user.is_authenticated:
            db_cart, created = DBCart.objects.get_or_create(customer=user)
            try:
                cart_item = CartItem.objects.get(cart=db_cart, product=product)
                if action == 'plus':
                    cart_item.quantity += 1
                elif action == 'minus' and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                cart_item.save()
            except:
                pass
        else:
            product_id = str(product.id)

            if product_id in self.cart:
                if action == 'plus':
                    self.cart[product_id]['quantity'] += 1
                elif action == 'minus' and self.cart[product_id]['quantity'] > 1:
                    self.cart[product_id]['quantity'] -= 1
                self.save()

    def get_total_price(self):
        price = 0
        user = self.request.user

        if user.is_authenticated:
            db_cart, created = DBCart.objects.get_or_create(customer=user)
            price = db_cart.get_total_price
        else:
            for product_id in self.cart:
                item = Product.objects.get(id=product_id)
                price += self.cart[product_id]['quantity'] * item.price

        return price

    def get_items(self):
        user = self.request.user

        if user.is_authenticated:
            db_crt, created = DBCart.objects.get_or_create(customer=user)
            items = db_crt.cartitem_set.all()
        else:
            items = []
            for i in self.cart:
                quantity = self.cart[i]['quantity']
                product = Product.objects.get(id=i)
                total_price = product.price * quantity
                items.append({
                    'product': product,
                    'get_total_price': total_price,
                    'quantity': quantity
                })
            # product_ids = self.cart.keys()
            # cart = self.cart.copy()

            # products = Product.objects.filter(id__in=product_ids)
            
            # for product in products:
            #     cart[str(product.id)]['product'] = product
            #     cart[str(product.id)]['price'] = product.price

            # for item in cart.values():
            #     item['get_total_price'] = item['price'] * item['quantity']
            #     yield item
        return items

    def delete(self, product):
        user = self.request.user

        if user.is_authenticated:
            db_cart, created = DBCart.objects.get_or_create(customer=user)
            try:
                CartItem.objects.get(cart=db_cart, product=product).delete()
            except:
                pass
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
        self.session.save()
