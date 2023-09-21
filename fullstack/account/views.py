from django.forms.models import BaseModelForm
from django.views.generic import ListView, CreateView, UpdateView, FormView
from .models import User
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm, UserUpdateForm, 
    PasswordResetConfirmForm, PasswordResetForm,
    CustomAuthenticationForm
)
from django.contrib.auth.views import PasswordChangeView
from order.models import Order
from address.models import Address
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


class SignupView(CreateView):
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

        return redirect('login')


class CustomPasswordResetView(PasswordResetView):
    template_name = "auth/passwordReset.html"
    email_template_name = 'email/resetPassword.html'
    subject_template_name = 'email/resetPasswordSubject.txt'
    html_email_template_name = 'email/resetPassword.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/passwordResetDone.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/passwordResetConfirm.html"
    success_url = reverse_lazy('login')
    # form_class = PasswordResetConfirmForm
    post_reset_login = True

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Пароль обновлен')
        return super().form_valid(form)


class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'adm/userList.html'

    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            raise Http404
        return True


class AccountView(LoginRequiredMixin, ListView):
    template_name = 'usage/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(customer=self.request.user, is_deleted=False)
        return context

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user)
        return queryset


class CustomPasswordChangeView(PasswordChangeView):
    template_name= "auth/changePassword.html"
    success_url= reverse_lazy('account')


# class UserUpdateView(UserPassesTestMixin, FormView):
    # template_name = 'usage/settings.html'
    # success_url = reverse_lazy('account')
    # model = User
    # form_class = UserUpdateForm

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

    # def test_func(self):
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         raise Http404
    #     return True


class UserUpdateView(UserPassesTestMixin, View):
    template_name = 'usage/settings.html'
    success_url = reverse_lazy('account')

    def get(self, request):
        return render(request, self.template_name, {'form': UserUpdateForm(instance=request.user)})

    def post(self, request):
        form = UserUpdateForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()

            return redirect('account')

        return render(request, self.template_name, {'form': form})

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            raise Http404
        return True