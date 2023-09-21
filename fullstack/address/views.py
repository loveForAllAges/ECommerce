from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddressForm
from .models import Address
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required
import json


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
    fields = ('name',)
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


@login_required
def address_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address_id = int(data['addressId'])
        Address.objects.filter(customer=request.user, id=address_id, is_deleted=False).update(is_deleted=True)
        return HttpResponse('Updated')
    
    raise Http404


@login_required
def address_make_main(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        address_id = int(data['addressId'])
        user = request.user
        Address.objects.filter(customer=user, is_main=True).update(is_main=False)
        Address.objects.filter(customer=user, id=address_id, is_main=False).update(is_main=True)
        return HttpResponse('Updated')

    raise Http404