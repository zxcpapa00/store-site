from django.contrib import admin

from products.models import Basket

from .models import EmailVerification, User


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'create_time')
    readonly_fields = ('create_time',)
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verification')
    inlines = (BasketAdmin, )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    readonly_fields = ('created', )
