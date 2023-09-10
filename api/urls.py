from django.urls import path, include
from .views import ProductModelViewSet, CategoryModelViewSet, BasketModelViewSet
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'category', CategoryModelViewSet)
router.register(r'basket', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

