from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddressForm
from .models import Address
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


class AddressView(UserPassesTestMixin, View):
    template_name = 'usage/addresses.html'
    
    def get(self, request):
        context = {
            'object_list': Address.objects.filter(customer=request.user, is_deleted=False),
            'form': AddressForm
        }
        return render(self.request, self.template_name, context)

    def post(self, request):
        data = request.POST
        form = AddressForm(data)

        if form.is_valid():
            Address.objects.create(city=data.get('address'), address=data.get('address'), customer=request.user)
            messages.add_message(request, messages.SUCCESS, 'Адрес сохранен')
        else:
            messages.add_message(request, messages.ERROR, 'Введены неверные данные')
        return redirect('address')

    def test_func(self):
        if  self.request.user.is_anonymous:
            raise Http404
        return True


class AddressDeleteView(UserPassesTestMixin, View):
    model = Address
    success_url = reverse_lazy('account')
    template_name = 'usage/addresses.html'

    def post(self, request, pk):
        Address.objects.filter(customer=request.user, id=pk, is_deleted=False).update(is_deleted=True, is_main=False)
        messages.add_message(request, messages.SUCCESS, 'Адрес удален')
        return redirect('address')
    
    def test_func(self):
        pk = self.kwargs.get('pk')
        item = Address.objects.filter(id=pk)
        user = self.request.user
        if self.request.user.is_anonymous or not item or item[0].customer != user:
            # messages.add_message(self.request, messages.ERROR, 'Ошибка удаления адреса')
            return False
        return True
