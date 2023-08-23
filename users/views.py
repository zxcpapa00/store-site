from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from products.models import Basket
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to=reverse('products:index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Вы успешно зарегистрировались!')
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        'baskets': Basket.objects.filter(user__username=request.user.username)
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(redirect_to=reverse('products:index'))



