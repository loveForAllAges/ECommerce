from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='main'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('adm/products/create/', views.CreateProductView.as_view(), name='create-product'),
    path('adm/products/update/<int:pk>/', views.UpdateProductView.as_view(), name='update-product'),
    path('adm/products/delele/<int:pk>/', views.DeleteProductView.as_view(), name='delete-product'),

    path('adm/create-category/', views.CreateCategoryView.as_view(), name='create-category'),
    # path('delele-category/<int:id>/', views.DeleteCategoryView.as_view(), name='delete-category'),

    path('adm/create-size/', views.CreateSizeView.as_view(), name='create-size'),
    # path('delele-size/<int:id>/', views.DeleteSizeView.as_view(), name='delete-size'),

    path('adm/create-brand/', views.CreateBrandView.as_view(), name='create-brand'),
    # path('delete-brand/<int:id>/', views.DeleteBrandView.as_view(), name='delete-brand'),
]
