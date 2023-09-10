import stripe

from django.db import models
from django.conf import settings

from users.models import User

stripe.api_key = settings.STRIPE_SECRET


class Category(models.Model):
    """Категории"""
    name = models.CharField(verbose_name='Название категории', max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


def get_image_path(instance, filename):
    """Функция динамического upload_to для Product"""
    return 'products/{0}/{1}'.format(instance.category.name, filename)


class Product(models.Model):
    """Товар"""
    name = models.CharField(verbose_name='Название товара', max_length=256)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='В наличие', default=0)
    image = models.ImageField(verbose_name='Изображение', upload_to=get_image_path, blank=True)
    stripe_product_id = models.CharField(max_length=256, null=True, blank=True)
    category = models.ForeignKey(to=Category, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_id:
            stripe_product_price = self.create_stripe_product()
            self.stripe_product_id = stripe_product_price['id']
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum_price() for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    """Корзина"""
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для - {self.user.username} | Товар {self.product.name}'

    def sum_price(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum_price': float(self.sum_price())
        }
        return basket_item
