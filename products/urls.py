from django.urls import path
from .views import index, products, basket_add

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('products/', products, name='products'),
    path('products/page=<int:page>', products, name='paginator'),
    path('products/<str:category_name>', products, name='filter'),
    path('products/<str:category_name>/page=<int:page>', products, name='filter_paginator'),
    path('products/add/<int:product_id>', basket_add, name='basket_add'),
]
