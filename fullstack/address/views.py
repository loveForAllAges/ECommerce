from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddressForm
from .models import Address
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'usage/addressCreate.html'
    success_url = reverse_lazy('account')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.customer = self.request.user
        return super().form_valid(form)
    

class AddressUpdateView(UserPassesTestMixin, UpdateView):
    model = Address
    fields = ('address',)
    template_name = 'usage/addressCreate.html'
    success_url = reverse_lazy('account')

    def test_func(self):
        pk = self.kwargs.get('pk')
        item = Address.objects.get(id=pk)
        user = self.request.user
        if not user.is_authenticated or not item.customer == user:
            raise Http404
        return True


class AddressDeleteView(UserPassesTestMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('account')
    template_name = ''

    def test_func(self):
        pk = self.kwargs.get('pk')
        item = Address.objects.get(id=pk)
        user = self.request.user
        if not self.request.user.is_authenticated or not item.customer == user:
            raise Http404
        return True
