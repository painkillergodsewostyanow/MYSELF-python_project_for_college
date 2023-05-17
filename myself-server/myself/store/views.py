from django.shortcuts import render
from store.forms import *


def index(request):
    return render(request, 'store/index.html')


def book_certificate(request):
    if request.method == "POST":
        form = BookCertificate(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BookCertificate()

    context = {
        'form': form
    }
    return render(request, 'store/certificate.html', context)


def search(request):
    return render(request, 'store/search.html')
