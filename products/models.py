from django.db import models


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
    image = models.ImageField(verbose_name='Изображение', upload_to=get_image_path)
    category = models.ForeignKey(to=Category, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


