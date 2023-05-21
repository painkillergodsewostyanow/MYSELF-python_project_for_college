from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from user.forms import *
from user.models import *
from django.contrib.auth import logout as login_out


def reg(request):
    if request.method == 'POST':
        form = UserRegForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user:log"))
    else:
        form = UserRegForm()
    context = {
        'form': form,
        'button_title': "СОЗДАТЬ АККАУНТ",
        'action_title': "Отмена",
        'title': "Регистрация",
        'action': 'user:reg',
        'is_enter_chosen': False
    }
    return render(request, 'user/reg.html', context)


def log(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'button_title': "ВОЙТИ",
        'action_title': "Забыи пароль?",
        'title': "Авторизация",
        'action': 'user:log',
        'is_enter_chosen': True
    }

    return render(request, 'user/log.html', context)


def logout(request):
    login_out(request)
    return HttpResponseRedirect(reverse('store:home'))


def show_favorite(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:log'))

    context = {

        'title': "Избранное",
        'path': 'Главная - Избранное',
        'favorites': Favorite.objects.filter(user=request.user)

    }

    return render(request, 'user/favorite.html', context)


def add_to_favorite(request, product_id):
    product = Product.objects.get(id=product_id)
    favorites = Favorite.objects.filter(user=request.user, product=product)

    if not favorites.exists():
        Favorite.objects.create(user=request.user, product=product, quantity=1)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def del_from_favorite(request, favorite_id):
    favorite = Favorite.objects.get(id=favorite_id)
    favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def profile(request):
    return render(request, 'user/profile.html')
