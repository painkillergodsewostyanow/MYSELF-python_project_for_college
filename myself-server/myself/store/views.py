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


def catalog(request, sex=None, category_id=None, max_price=None, min_price=None):
    products = Product.objects.all()
    if sex:
        products = products.filter(sex=sex)

    if category_id:
        products = products.filter(category_id=category_id)

    context = {'products': products}
    print(context)
    return render(request, 'store/base_catalog.html', context)
