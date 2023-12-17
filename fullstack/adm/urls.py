from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.AdmView.as_view(), name='adm_home'),
    path('accounts/', views.AccountListView.as_view(), name='adm_account_list_api'),
    path('accounts/<int:pk>/', views.AccountDetailView.as_view(), name='adm_account_detail_api'),

    # path('chat/', views.ChatList.as_view(), name='chat-list'),
    # path('chat/<uuid:pk>/', views.ChatDetail.as_view(), name='chat-detail'),

    path('products/', views.ProductListView.as_view(), name='adm_product_list_api'),
]
