from typing import Any
from django.forms.models import BaseModelForm
from django.views.generic import ListView, CreateView, UpdateView, FormView
from .models import User
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm, UserUpdateForm, 
    CustomSetPasswordForm, CustomPasswordResetForm,
    CustomAuthenticationForm, CustomPasswordChangeForm
)
from django.contrib.auth.views import PasswordChangeView
from order.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponse
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
import threading
from .utils import account_activation_token
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, LoginView
from django.contrib.auth import login


class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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

        current_site = get_current_site(self.request)
        email_body = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        
        link = reverse('activate', kwargs={
                       'uidb64': email_body['uid'], 'token': email_body['token']})
        
        email_body.update({'url': 'http://'+current_site.domain+link})
        
        email_subject = 'Активация аккаунта'
        html_content = render_to_string('email/activateAccount.html', email_body)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            email_subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.attach_alternative(html_content, "text/html")
        EmailThread(email).start()

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


class AccountView(LoginRequiredMixin, View):
    template_name = 'usage/account.html'
    success_url = reverse_lazy('account')

    def get(self, request):
        return render(request, self.template_name)
    

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
