from django.urls import path
from .views import *


urlpatterns = [
    path('account', AccountAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('signup', SignupAPIView.as_view()),
    path('init', InitAPIView.as_view()),
    path('settings', SettingsAPIView.as_view()),
    path('change_password', ChangePasswordAPIView.as_view()),
    path('password_reset', PasswordResetAPIView.as_view()),
    path('password_reset/<uidb64>/<token>/', PasswordResetProcessAPIView.as_view()),
]
