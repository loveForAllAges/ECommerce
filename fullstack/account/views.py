# from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views import View
from .models import User
from django.urls import reverse_lazy
from .forms import SignupForm, UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.forms import PasswordChangeForm
from order.models import Order, Address
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class SignupView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('main')


class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'adm/userList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class AccountView(LoginRequiredMixin, ListView):
    template_name = 'usage/account.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(customer=self.request.user)
        return context

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user).exclude(status=1)
        return queryset


class MyPasswordChangeView(PasswordChangeView):
    template_name= "auth/change-password.html"
    success_url= reverse_lazy('account')

# class UserCreateView(UserPassesTestMixin, CreateView):
#     template_name = 'adm/userCreate.html'
#     form_class = CreateView
#     success_url = reverse_lazy('user-list')

#     def test_func(self):
#         if not self.request.user.is_authenticated or not self.request.user.is_staff:
#             raise Http404
#         return True


# class UserUpdateView(UserPassesTestMixin, UpdateView):
#     model = User
#     form_class = UserUpdateForm
#     template_name = 'adm/userUpdate.html'
#     success_url = reverse_lazy('user-list')

#     def test_func(self):
#         if not self.request.user.is_authenticated or not self.request.user.is_staff:
#             raise Http404
#         return True


# class UserDeleteView(UserPassesTestMixin, DeleteView):
#     model = User
#     success_url = reverse_lazy('user-list')
#     template_name = ''

#     def test_func(self):
#         if not self.request.user.is_authenticated or not self.request.user.is_staff:
#             raise Http404
#         return True
