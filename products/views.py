from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView

from common.views import TitleMixin

from .models import Basket, Category, Product


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Главная страница'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 2
    context_object_name = 'products'
    title = 'Каталог'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = cache.get('categories')
        if not categories:
            context['categories'] = Category.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.kwargs.get('category_name')
        return queryset.filter(category__name=category_name) if category_name else queryset


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
