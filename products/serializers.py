from rest_framework import serializers, fields
from .models import Product, Category, Basket
from users.models import User


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum_price = fields.FloatField()
    total_sum = fields.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum_price', 'total_sum', 'user', 'create_time')
        read_only_fields = ('create_time', )

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()
