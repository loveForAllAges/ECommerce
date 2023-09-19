from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path("change-password/", views.MyPasswordChangeView.as_view(), name='change-password'),

    path('adm/users/', views.UserListView.as_view(), name='user-list'),
    # path('adm/users/create/', views.UserCreateView.as_view(), name='user-create'),
    # path('adm/users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    # path('adm/users/delele/<int:pk>/', views.UserDeleteView.as_view(), name='user-delete'),
]
