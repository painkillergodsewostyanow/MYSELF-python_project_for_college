from django.urls import path

from store.views import *

app_name = 'store'

urlpatterns = [
    path('', index, name='home'),
    path('book_certificate', book_certificate, name='book_certificate'),
    path('search', search, name='search'),
    path('catalog', catalog, name='catalog'),
    path('catalog/sex/<int:sex>', catalog, name='catalog_filters'),
    path('catalog/category/<int:category_id>', catalog, name='catalog_by_category'),
    path('catalog/sex/<int:sex>/category/<int:category_id>', catalog, name='catalog_by_filter'),
]
