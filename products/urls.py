from django.urls import path

from .views import IndexView, ProductListView, basket_add

app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<str:category_name>', ProductListView.as_view(), name='filter'),
    path('products/add/<int:product_id>', basket_add, name='basket_add'),
]
