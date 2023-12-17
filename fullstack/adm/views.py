from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from product.models import Product, ProductImage
from django.http import Http404
from product.forms import ProductForm
from django.views import View, generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from utils.imageManager import isImage, squareTheImage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from product.models import Category, Brand
from product.forms import CategoryForm, BrandForm
from account.models import User
from order.models import Order
# from chat.models import Chat
from django.db.models import Count
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Sum, F


class StaffOnly(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool | None:
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        raise Http404


# class ChatList(StaffOnly, generic.ListView):
#     template_name = 'adm/chat_list.html'
#     queryset = Chat.objects.annotate(num_messages=Count('messages')).filter(num_messages__gt=0).order_by('-created_at')


# class ChatDetail(StaffOnly, View):
#     template_name = 'adm/chat_list.html'

#     def __get_data(self, request, pk):
#         context = dict()
#         context['object'] = Chat.objects.get(pk=pk)
#         context['object_list'] = Chat.objects.annotate(num_messages=Count('messages')).filter(
#         Q(num_messages__gt=0) & (Q(agent__isnull=True) | Q(agent=request.user))).order_by('-created_at')
#         return context
    
#     def get(self, request, pk):
#         return render(request, self.template_name, context=self.__get_data(request, pk))
    
#     def post(self, request, pk):
#         pk = request.POST.get('chat_id', None)
#         print(pk)
#         chat = get_object_or_404(Chat, pk=pk, agent__isnull=True)
#         chat.agent = request.user
#         chat.status = 1
#         chat.save()

#         return render(request, self.template_name, context=self.__get_data(request, pk))


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_superuser
    

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)


class AdmView(AdminRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        users = User.objects.all()

        context = {
            'orders': {
                'total': len(orders.filter()),
                'active': len(orders.filter(status__in=[0,1,2,3])),
                'closed': len(orders.filter(status=4)),
                'cancelled': len(orders.filter(status=5)),
            },
            'users': {
                'total': len(users),
                'new': len(users.filter(date_joined__date=date.today())),
                'adm': len(users.filter(is_superuser=True)),
                'staff': len(users.filter(is_staff=True)),
            }
        }

        print(context)
        return render(request, 'adm/home.html', context=context)


class AccountListView(AdminRequiredMixin, generic.ListView):
    model = User
    template_name = 'adm/account_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return User.objects.filter(is_active=True)


class AccountDetailView(AdminRequiredMixin, generic.DetailView):
    model = User
    template_name = 'usage/account.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['object_list'] = Order.objects.filter(customer_id=self.kwargs.get('pk')).order_by('-number')
        return context


class ProductListView(AdminRequiredMixin, generic.ListView):
    model = Product
    template_name = 'adm/product_list.html'


class ProductCreateView(AdminRequiredMixin, View):
    template_name = 'adm/productCreate.html'
    form_class = ProductForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        photos = request.FILES.getlist('photos')
        error = False
        for photo in photos:
            if not isImage(photo):
                error = True
                messages.add_message(request, messages.ERROR, 'Файл не является изображением')
                break

        if form.is_valid() and photos and not error:
            product = form.save(commit=False)
            product.save()
            for photo in photos:
                new_filename, new_image = squareTheImage(photo)
                print(new_filename, new_image)
                new_photo = ProductImage.objects.create(product=product)
                new_photo.image.save(new_filename, new_image, save=False)

                new_photo.save()
                
            return redirect('product-list')
        return render(request, self.template_name, {'form': form})




class ProductUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adm/productCreate.html'
    success_url = reverse_lazy('product-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class ProductDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('product-list')
    template_name = ''

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
  

class CategoryListView(UserPassesTestMixin, generic.ListView):
    model = Category
    template_name = 'adm/categoryList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class CategoryCreateView(UserPassesTestMixin, generic.CreateView):
    template_name = 'adm/categoryCreate.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class CategoryUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'adm/categoryCreate.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class CategoryDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    template_name = ''

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class BrandListView(UserPassesTestMixin, generic.ListView):
    model = Brand
    template_name = 'adm/brandList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class BrandCreateView(UserPassesTestMixin, generic.CreateView):
    template_name = 'adm/brandCreate.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class BrandUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Brand
    fields = '__all__'
    template_name = 'adm/brandCreate.html'
    success_url = reverse_lazy('brand-list')

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
    

class BrandDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Brand
    success_url = reverse_lazy('brand-list')
    template_name = ''

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True
