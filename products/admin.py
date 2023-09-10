from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'get_image')
    fields = ('name', 'description', ('image', 'get_image'), ('price', 'quantity'), 'category', 'stripe_product_id')
    search_fields = ('name', )
    list_filter = ('category', )
    ordering = ('name', )
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'
