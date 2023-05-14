from django.urls import path

from store.views import *

app_name = 'store'

urlpatterns = [
    path('', index, name='home'),
    path('book_certificate', book_certificate, name='book_certificate'),
]
