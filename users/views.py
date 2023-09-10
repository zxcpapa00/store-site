from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegisterForm
from .models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    """Класс авторизации"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'

    def post(self, request, *args, **kwargs):
        form = self.get_form(form_class=UserLoginForm)
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        if form.is_valid():
            if user.is_verification:
                return self.form_valid(form)
            else:
                messages.error(request, 'Подтвердите вашу почту!')
                return HttpResponseRedirect(reverse('users:login'))
        else:
            return self.form_invalid(form)


class UserRegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    """Класс регистрации"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы. Чтобы завершить регистрацию подтвердите вашу почту'
    title = 'Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    """Класс профиля пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(code=code, user=user)
        if email_verification.exists() and not email_verification.last().is_expired():
            user.is_verification = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('products:index'))
