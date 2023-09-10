from django.test import TestCase
from django.urls import reverse

from products.models import Product, Category


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Главная страница')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsViewTestCase(TestCase):

    fixtures = ['categories.json', 'goods.json']

    def test_products(self):
        path = reverse('products:products')
        response = self.client.get(path)

        products = list(Product.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), products[:2])

    def test_products_with_category(self):
        category = Category.objects.first()
        path = reverse('products:filter', kwargs={'category_name': category.name})
        response = self.client.get(path)

        products = Product.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(
            list(response.context_data['object_list']),
            list(products.filter(category=category)[:2])
        )





