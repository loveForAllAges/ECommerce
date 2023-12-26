from django.urls import path
from .views import *


urlpatterns = [
    # path("password-change/", CustomPasswordChangeView.as_view(), name='password-change'),

    # path("password-reset/", views.CustomPasswordResetView.as_view(),name="password_reset"),
    # path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # # path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('account', AccountAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('signup', SignupAPIView.as_view()),
    path('init', InitAPIView.as_view()),
    path('settings', SettingsAPIView.as_view()),
    path('change_password', ChangePasswordAPIView.as_view()),
]
