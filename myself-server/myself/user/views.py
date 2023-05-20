from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from user.forms import *
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


def favorite(request):
    return render(request, 'user/favorite.html')


def profile(request):
    return render(request, 'user/profile.html')
