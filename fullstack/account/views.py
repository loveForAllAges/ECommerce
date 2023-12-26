from .forms import (
    CustomSetPasswordForm, CustomPasswordResetForm,
)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, 
)

from config.utils import send_email
from rest_framework.authtoken.models import Token


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


# class UserListView(UserPassesTestMixin, ListView):
#     model = User
#     template_name = 'adm/userList.html'

#     def test_func(self):
#         if not self.request.user.is_authenticated or not self.request.user.is_staff:
#             raise Http404
#         return True


from product.utils import preview_product_queryset
from account.serializers import (
    AccountSerializer, UserSerializer, User, SettingsSerializer, 
    PasswordChangeSerializer
)
from order.models import OrderItem, Order

from django.db.models import Prefetch
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash

from rest_framework import (
    views, status, permissions, generics
)
from rest_framework.response import Response
from product.decorators import cart_and_categories


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

    @cart_and_categories
    def get(self, request):
        serializer = AccountSerializer(self.get_queryset(), context={'request': request})
        return Response({'content': serializer.data}, status=status.HTTP_200_OK)


class LoginAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        response = dict()
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            response['token'] = 'Token ' + token.key
            response['redirect_url'] = reverse_lazy('account_detail')
        else:
            response['error'] = 'Неверный логин или пароль'
        return Response(response)


class SignupAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        send_email(request, user, 'Регистрация', f'Подтвердить регистрацию: ', url=True)
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)


class InitAPIView(views.APIView):
    @cart_and_categories
    def get(self, request, *args, **kwargs):
        return Response(dict())


class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        response = {'redirect_url': reverse_lazy('login')}
        return Response(response, status=status.HTTP_200_OK)


class SettingsAPIView(views.APIView):
    @cart_and_categories
    def get(self, request, *args, **kwargs):
        serializer = SettingsSerializer(request.user)
        return Response({'content': serializer.data})
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = SettingsSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'Изменения сохранены'}
        return Response(response)


class ChangePasswordAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        update_session_auth_hash(self.request, user)
        return Response({'message': 'Пароль изменен'})
