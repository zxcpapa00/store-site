from django.urls import path
from .views import OrderCreateView, SuccessView, CancelView, OrdersView, DetailOrderView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('', OrdersView.as_view(), name='all-orders'),
    path('<int:pk>', DetailOrderView.as_view(), name='detail-order'),
]

