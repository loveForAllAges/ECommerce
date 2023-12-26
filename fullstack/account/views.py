from django.db.models import Prefetch
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import (
    views, status, permissions, generics
)

from product.utils import preview_product_queryset
from order.models import OrderItem, Order
from config.utils import account_activation_token, send_email, decode_user
from product.decorators import cart_and_categories
from account.serializers import (
    AccountSerializer, UserSerializer, User, SettingsSerializer, 
    PasswordChangeSerializer, PasswordResetSerializer
)


# class UserListView(UserPassesTestMixin, ListView):
#     model = User
#     template_name = 'adm/userList.html'

#     def test_func(self):
#         if not self.request.user.is_authenticated or not self.request.user.is_staff:
#             raise Http404
#         return True


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
            response['redirect_url'] = reverse('account_detail')
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

        url = reverse(
            'activate', 
            kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': account_activation_token.make_token(user)
            }
        )

        send_email(
            user.email, 
            'Регистрация',
            f'Подтвердить регистрацию: ' + request.build_absolute_uri(url)
        )
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
        response = {'redirect_url': reverse('login')}
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


class PasswordResetAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email_reset', '')
        try:
            user = User.objects.get(email=email)

            url = reverse(
                'password_reset_process', 
                kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 
                    'token': account_activation_token.make_token(user)
                }
            )

            send_email(
                user.email, 
                'Сброс пароля',
                f'Ссылка для сброса пароля: ' + request.build_absolute_uri(url)
            )
        except Exception as ex:
            print(ex)
        return Response({})


class PasswordResetProcessAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        print(args, kwargs)
        print(request.data)
        user = decode_user(kwargs['uidb64'], kwargs['token'])
        print('USER', user)
        serializer = PasswordResetSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'redirect_url': reverse('login')})
