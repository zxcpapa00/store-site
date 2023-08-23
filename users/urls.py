from django.urls import path
from .views import *
from products.views import basket_remove

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('remove/<int:basket_id>', basket_remove, name='remove'),
    path('logout/', logout, name='logout'),
    path('registration/', register, name='register'),
    path('profile/', profile, name='profile'),
]

