from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from store.models import *
from store.forms import *


def index(request):
    return render(request, 'store/index.html')


def book_certificate(request):
    if request.method == "POST":
        form = BookCertificate(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store:home'))
    else:
        form = BookCertificate()

    context = {
        'form': form
    }
    return render(request, 'store/certificate.html', context)


def search(request):
    return render(request, 'store/search.html')


def catalog(request, sex=None, category_id=None, max_price=None, min_price=None, sale=None):
    products = Product.objects.all()
    if sex:
        products = products.filter(sex=sex)
        if sex != 3:
            sex_str_repr = ' - Мужская одежда' if sex == 1 else ' - Женская одежда'
        else:
            sex_str_repr = "Унисекс"
    else:
        sex_str_repr = ""
    if category_id:
        products = products.filter(category_id=category_id)
        category_str_repr = '' if ProductCategory.objects.get(pk=category_id) is None else \
            ' - ' + ProductCategory.objects.get(pk=category_id).name
    else:
        category_str_repr = ''

    side_img = ['/static/img/catalog/side_img2.jpg', '/static/img/catalog/side_img1.jpg'] if sex==2\
        else ['/static/img/catalog/side_img3.jpg']

    path = f"Каталог{sex_str_repr}{category_str_repr}"
    title = f"Каталог {sex_str_repr}"
    context = {'products': products, 'title': title, 'path': path, 'side_img': side_img}
    return render(request, 'store/base_catalog.html', context)
