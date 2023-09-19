# from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.conf import settings
from django.urls import reverse_lazy
from .forms import SignupForm
# from django.contrib.auth.forms import UserCreationForm


class SignupView(CreateView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('main')


# class AccountView(LoginRequiredMixin, View):
#     pass


# class UserListView(ListView):
#     model = settings.AUTH_USER_MODEL
#     template_name = 'adm/userList.html'


# class UserCreateView(CreateView):
#     template_name = 'adm/userCreate.html'
#     # form_class = BrandForm
#     success_url = reverse_lazy('user-list')


# class UserUpdateView(UpdateView):
#     model = settings.AUTH_USER_MODEL
#     fields = '__all__'
#     template_name = 'adm/userCreate.html'
#     success_url = reverse_lazy('user-list')


# class UserDeleteView(DeleteView):
#     model = settings.AUTH_USER_MODEL
#     success_url = reverse_lazy('user-list')
#     template_name = ''
