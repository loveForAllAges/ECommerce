from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.AdmView.as_view(), name='adm'),
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', views.AccountDetailView.as_view(), name='account-detail'),

    path('chat/', views.ChatList.as_view(), name='chat-list'),
    path('chat/<uuid:pk>/', views.ChatDetail.as_view(), name='chat-detail'),

    # path('adm/orders/', views.OrderListView.as_view(), name='order-list'),
    # path('adm/orders/create/', views.OrderListView.as_view(), name='order-create'),
    # path('adm/orders/<int:pk>/', views.OrderListView.as_view(), name='order-detail'),
    # path('adm/orders/update/<int:pk>/', views.OrderListView.as_view(), name='order-update'),
    # path('adm/orders/delete/<int:pk>/', views.OrderListView.as_view(), name='order-delete'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('adm/products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('adm/products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('adm/products/delele/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),

    path('adm/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('adm/categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('adm/categories/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('adm/categories/delele/<int:pk>/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('adm/brands/', views.BrandListView.as_view(), name='brand-list'),
    path('adm/brands/create/', views.BrandCreateView.as_view(), name='brand-create'),
    path('adm/brands/update/<int:pk>/', views.BrandUpdateView.as_view(), name='brand-update'),
    path('adm/brands/delete/<int:pk>/', views.BrandDeleteView.as_view(), name='brand-delete'),
]
