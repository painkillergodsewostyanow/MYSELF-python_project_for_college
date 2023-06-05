from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse, reverse_lazy
from user.forms import *
from user.models import *
from myself.settings import LOGIN_URL
from store.models import Size


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'user/reg.html'
    success_url = reverse_lazy("user:log")

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['button_title'] = "СОЗДАТЬ АККАУНТ"
        context['action_title'] = "Отмена"
        context['title'] = "Регистрация"
        context['action'] = "user:reg"
        context['is_enter_chosen'] = False
        return context


# def reg(request):
#     if request.method == 'POST':
#         form = UserRegForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("user:log"))
#     else:
#         form = UserRegForm()
#
#     context = {
#         'form': form,
#         'button_title': "СОЗДАТЬ АККАУНТ",
#         'action_title': "Отмена",
#         'title': "Регистрация",
#         'action': 'user:reg',
#         'is_enter_chosen': False
#     }
#     return render(request, 'user/reg.html', context)
#


class UserLoginView(LoginView):
    template_name = 'user/log.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['button_title'] = "ВОЙТИ"
        context['action_title'] = "Забыи пароль?"
        context['title'] = "Авторизация"
        context['action'] = "user:log"
        context['is_enter_chosen'] = True
        return context


# def log(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect('/')
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'form': form,
#         'button_title': "ВОЙТИ",
#         'action_title': "Забыи пароль?",
#         'title': "Авторизация",
#         'action': 'user:log',
#         'is_enter_chosen': True
#     }
#
#     return render(request, 'user/log.html', context)

# USE BASE LOGOUT VIEW FROM DJANGO
# def logout(request):
#     login_out(request)
#     return HttpResponseRedirect(reverse('store:home'))


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'user/favorite.html'
    login_url = 'user/reg'

    def get_context_data(self, **kwargs):
        context = super(FavoriteListView, self).get_context_data()
        context['title'] = 'Избранное'
        context['path'] = 'Избранное'
        return context

    def get_queryset(self):
        queryset = super(FavoriteListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


# @login_required(login_url=LOGIN_URL)
# def show_favorite(request):
#
#     context = {
#
#         'title': "Избранное",
#         'path': "Избранное",
#         'favorites': Favorite.objects.filter(user=request.user)
#
#     }
#
#     return render(request, 'user/favorite.html', context)
#


@login_required(login_url=LOGIN_URL)
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


@login_required(login_url=LOGIN_URL)
def profile(request):
    return render(request, 'user/profile.html')


class EmailVerificationView(TemplateView):
    template_name = 'user/email_verification.html'
    is_success = True

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code).first()

        if email_verifications.is_expired():
            self.is_success = False
            email_verifications.code = uuid.uuid4()
            email_verifications.expiration = now() + timedelta(hours=4)
            email_verifications.save()
            email_verifications.send_verification_email(is_expired=True)
            return super(EmailVerificationView, self).get(request, *args, **kwargs)

        if email_verifications:
            user.is_email_verified = True
            user.save()
            certificates = Certificate.objects.filter(email_recipient=self.kwargs['email'])

            for certificate in certificates:
                certificate.user = user
                certificate.save()

            return super(EmailVerificationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmailVerificationView, self).get_context_data()
        if self.is_success:
            context['message'] = "Ваша почта на сайте Myself успешно подтверждена!"
        else:
            context['message'] = "К сожалению ссылка устарела, на почту отправлена новая"
        return context


@login_required(login_url=LOGIN_URL)
def basket_add(request):
    product = Product.objects.get(title=Product.objects.get(pk=request.POST['product_id']).title,
                                  size=request.POST['size'])
    basket = Basket.objects.filter(user=request.user, product=product)
    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    Basket.objects.get(pk=basket_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])