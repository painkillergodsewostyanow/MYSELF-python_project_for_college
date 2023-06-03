from django.urls import path

from store.views import *

app_name = 'store'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('book_certificate', BookCertificateCreateView.as_view(), name='book_certificate'),
    path('search', search, name='search'),
    path('catalog', CatalogListView.as_view(), name='catalog'),
    path('catalog/sex/<int:sex>', CatalogListView.as_view(), name='catalog_filters'),
    path('catalog/category/<int:category_id>', CatalogListView.as_view(), name='catalog_by_category'),
    path('catalog/sex/<int:sex>/category/<int:category_id>', CatalogListView.as_view(), name='catalog_by_filter'),
    path('catalog/<int:pk>', ProductDetailView.as_view(), name='product_detail')
]
