from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from products.views import basket_remove

from .views import (EmailVerificationView, UserLoginView, UserProfileView,
                    UserRegisterView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('remove/<int:basket_id>', basket_remove, name='remove'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verify'),
]
