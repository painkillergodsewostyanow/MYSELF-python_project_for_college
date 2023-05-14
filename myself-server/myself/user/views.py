from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from user.forms import *


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
        'button_title': "Отправить",
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
        'button_title': "войти",
        'action_title': "Забыли пароль?",
        'title': "Авторизация",
        'action': 'user:log',
        'is_enter_chosen': True
    }

    return render(request, 'user/log.html', context)
