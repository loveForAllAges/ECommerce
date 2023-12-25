from config.utils import account_activation_token
from .models import User
from .forms import (
    CustomUserCreationForm, UserUpdateForm, 
    CustomSetPasswordForm, CustomPasswordResetForm,
    CustomAuthenticationForm, CustomPasswordChangeForm
)

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Exists, OuterRef
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, 
    LoginView, PasswordChangeView
)

from config.utils import send_email


class CustomLoginView(LoginView):
    template_name='auth/login.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm


class SignupView(UserPassesTestMixin, CreateView):
    template_name = 'auth/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        send_email(self.request, user, 'Активация аккаунта', f'Аккаунт создан. Подтвердите это, перейдя по ссылке: ', url=True)
        messages.add_message(self.request, messages.SUCCESS, 'Аккаунт создан! Проверьте почту для активации аккаунта')
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            raise Http404
        return True


class ActivationView(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=id)

        if not account_activation_token.check_token(user, token) or user.is_active:
            raise Http404

        messages.add_message(request, messages.SUCCESS, 'Аккаунт активирован!')

        user.is_active = True
        login(request, user)
        user.save()

        return redirect('account')


class CustomPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = "auth/passwordReset.html"
    email_template_name = 'email/resetPassword.html'
    subject_template_name = 'email/resetPasswordSubject.txt'
    html_email_template_name = 'email/resetPassword.html'
    form_class = CustomPasswordResetForm
    
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            raise Http404
        return True
    

class CustomPasswordResetDoneView(UserPassesTestMixin, PasswordResetDoneView):
    template_name = "auth/passwordResetDone.html"
    
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            raise Http404
        return True
    

class CustomPasswordResetConfirmView(UserPassesTestMixin, PasswordResetConfirmView):
    template_name = "auth/passwordResetConfirm.html"
    success_url = reverse_lazy('login')
    form_class = CustomSetPasswordForm
    post_reset_login = True

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Пароль обновлен!')
        return super().form_valid(form)
    
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            raise Http404
        return True


class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'adm/userList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class CustomPasswordChangeView(PasswordChangeView):
    template_name= "auth/passwordChange.html"
    success_url= reverse_lazy('account')
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Пароль обновлен!')
        return super().form_valid(form)


class AccountEditView(LoginRequiredMixin, View):
    template_name = 'auth/updateAccount.html'
    success_url = reverse_lazy('account')

    def get(self, request):
        return render(request, self.template_name, {'form': UserUpdateForm(instance=request.user)})

    def post(self, request):
        form = UserUpdateForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Изменения сохранены!')
            return redirect('account')

        return render(request, self.template_name, {'form': form})



from product.models import Product
from product.utils import preview_product_queryset
from account.models import User
from account.serializers import AccountSerializer
from order.models import OrderItem, Order

from django.db.models import Exists, OuterRef, Prefetch

from rest_framework import (
    response, views, status, permissions,
)


class AccountAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.prefetch_related(
            Prefetch('orders', queryset=Order.objects.prefetch_related(
                Prefetch('goods', queryset=OrderItem.objects.prefetch_related(
                    Prefetch('product', queryset=preview_product_queryset(self.request))
                ))
            )),
        ).get(id=self.request.user.id)
        return queryset

    def get(self, request):
        serializer = AccountSerializer(self.get_queryset(), context={'request': request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)
