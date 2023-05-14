from django.shortcuts import render


def index(request):
    return render(request, 'store/index.html')


def book_certificate(request):
    return render(request, 'store/certificate.html')


def search(request):
    return render(request, 'store/search.html')
