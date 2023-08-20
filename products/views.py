from django.shortcuts import render
from .models import *


def index(request):
    context = {
        'title': 'Главная страница',
        'user': request.user
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'products/products.html', context)
