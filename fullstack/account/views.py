# from django.shortcuts import render
# from django.views.generic import ListView, CreateView, DeleteView, UpdateView
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.conf import settings
# from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView


# class MyLoginView(LoginView):
#     template_name = 'usage/login.html'


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
