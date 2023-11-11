from django.conf import settings
from product.models import Product
from .models import Cart as DBCart, CartItem
from category.models import Size
from .serializers import CartItemSerializer, CartSerializer


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart
        # self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def add(self, product, size):
        user = self.request.user

        if user.is_authenticated:
            db_cart, created = DBCart.objects.get_or_create(customer=user)
            try:
                cart_item = CartItem.objects.get(cart=db_cart, product_id=product, size_id=size)
                cart_item.quantity += 1
                cart_item.save()
            except:
                CartItem.objects.create(cart=db_cart, product_id=product, size_id=size)
        else:
            current_product = next((i for i, d in enumerate(self.cart) if d['product_id'] == product and d['size_id'] == size), -1)

            if current_product >= 0:
                self.cart[current_product]['quantity'] += 1
            else:
                self.cart.append({'quantity': 1, 'size_id': size, 'product_id': product})

            self.save()

    def __len__(self):
        user = self.request.user
        
        if user.is_authenticated:
            db_crt, created = DBCart.objects.get_or_create(customer=user)
            return db_crt.size
        else:
            return sum([item['quantity'] for item in self.cart])

    def update(self, product, action, size):
        user = self.request.user

        if user.is_authenticated:
            try:
                is_deleted = False
                cart_item = CartItem.objects.get(cart__customer=user, product_id=product, size_id=size)
                if action == 'plus':
                    cart_item.quantity += 1
                elif action == 'minus' and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    cart_item.delete()
                    is_deleted = True
                if not is_deleted:
                    cart_item.save()
            except:
                pass
        else:
            current_product = next((i for i, d in enumerate(self.cart) if d['product_id'] == product.id and d['size_id'] == size.id), -1)
            print(current_product)
            if current_product >= 0:
                if action == 'plus':
                    self.cart[current_product]['quantity'] += 1
                elif action == 'minus' and self.cart[current_product]['quantity'] > 1:
                    self.cart[current_product]['quantity'] -= 1
                else:
                    del self.cart[current_product]
                self.save()

    def get_total_price(self):
        price = 0
        user = self.request.user

        if user.is_authenticated:
            db_cart, created = DBCart.objects.get_or_create(customer=user)
            price = db_cart.get_total_price
        else:
            for i in self.cart:
                item = Product.objects.get(id=i['product_id'])
                price += i['quantity'] * item.price

        return price

    def get_cart(self):
        user = self.request.user

        if user.is_authenticated:
            cart, created = DBCart.objects.get_or_create(customer=user)
            res = CartSerializer(cart, context={'request': self.request}).data
        else:
            res = []
            # for i in self.cart:
            #     quantity = i['quantity']
            #     product = Product.objects.get(id=i['product_id'])
            #     size = Size.objects.get(id=i['size_id'])
            #     total_price = product.price * quantity
            #     res.append({
            #         'product': product,
            #         'size': size,
            #         'get_total_price': total_price,
            #         'quantity': quantity
            #     })

        # print(res)
        return res
    
    def clear(self):
        user = self.request.user

        if user.is_authenticated:
            DBCart.objects.get(customer=user).delete()
        else:
            del self.session[settings.CART_SESSION_ID]
            self.save()

    def save(self):
        self.session.modified = True
        self.session.save()
