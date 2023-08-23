from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    context = {
        'title': 'Главная страница',
        'user': request.user
    }
    return render(request, 'products/index.html', context)


def products(request, category_name=None, page=1):
    products = Product.objects.filter(category__name=category_name) if category_name else Product.objects.all()
    paginator = Paginator(object_list=products, per_page=2)
    products_paginator = paginator.page(page)
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
        'products': products_paginator,
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



