from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from store.models import *
from store.forms import *
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from user.models import Favorite


class IndexView(TemplateView):
    template_name = 'store/index.html'


# def index(request):
#     return render(request, 'store/index.html')


class CatalogListView(ListView):
    model = Product
    template_name = 'store/catalog.html'

    def get_queryset(self):
        queryset = cache.get('queryset')

        if not queryset:
            queryset = super(CatalogListView, self).get_queryset()
            sex = self.kwargs.get('sex', None)
            category_id = self.kwargs.get('category_id', None)

            if sex:
                queryset = queryset.filter(sex=sex)

            if category_id:
                queryset = queryset.filter(category_id=category_id)

            cache.set('queryset', queryset, 30)

        return Product.del_duplicate_by_title(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogListView, self).get_context_data()
        sex = self.kwargs.get('sex', None)
        category_id = self.kwargs.get('category_id', None)

        if not sex:
            sex_str_repr = ""
        else:
            if sex != 3:
                sex_str_repr = ' - Мужская одежда' if sex == 1 else ' - Женская одежда'
            else:
                sex_str_repr = "Унисекс"

        if category_id:
            category_str_repr = '' if ProductCategory.objects.get(pk=category_id) is None else \
                ' - ' + ProductCategory.objects.get(pk=category_id).name
        else:
            category_str_repr = ""

        side_img = ['/static/img/catalog/side_img2.jpg', '/static/img/catalog/side_img1.jpg'] if sex == 2 \
            else ['/static/img/catalog/side_img3.jpg']

        path_filter = f"Каталог{sex_str_repr}{category_str_repr}"
        title = f"Каталог {sex_str_repr}"

        if self.request.user.is_authenticated:
            context['favorite'] = Favorite.get_favorite_product(user=self.request.user)

        context['title'] = title
        context['path'] = path_filter
        context['side_img'] = side_img
        return context


# TODO: fix
def product_detail(request, pk=None, color=None):
    context = {}
    favorite = Favorite.get_favorite_product(user=request.user) if request.user.is_authenticated else None
    if color:
        product = Product.objects.filter(title=Product.objects.get(pk=pk).title,
                                         color=Color.objects.get(color=color)).last()
    else:
        product = Product.objects.get(pk=pk)

    context['favorite_product'] = favorite
    context['product'] = product

    return render(request, 'store/product_detail.html', context)


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'store/product_detail.html'


# def catalog(request, sex=None, category_id=None, max_price=None, min_price=None, sale=None):
#     products = Product.objects.all()
#     if sex:
#         products = products.filter(sex=sex)
#         if sex != 3:
#             sex_str_repr = ' - Мужская одежда' if sex == 1 else ' - Женская одежда'
#         else:
#             sex_str_repr = "Унисекс"
#     else:
#         sex_str_repr = ""
#
#     if category_id:
#         products = products.filter(category_id=category_id)
#         category_str_repr = '' if ProductCategory.objects.get(pk=category_id) is None else \
#             ' - ' + ProductCategory.objects.get(pk=category_id).name
#     else:
#         category_str_repr = ''
#
#     side_img = ['/static/img/catalog/side_img2.jpg', '/static/img/catalog/side_img1.jpg'] if sex == 2\
#         else ['/static/img/catalog/side_img3.jpg']
#
#     path = f"Каталог{sex_str_repr}{category_str_repr}"
#     title = f"Каталог {sex_str_repr}"
#     context = {'products': products, 'title': title, 'path': path, 'side_img': side_img}
#     return render(request, 'store/catalog.html', context)


class BookCertificateCreateView(CreateView):
    model = Certificate
    template_name = 'store/certificate.html'
    success_url = reverse_lazy('store:home')
    form_class = BookCertificate


# def book_certificate(request):
#     if request.method == "POST":
#         form = BookCertificate(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('store:home'))
#     else:
#         form = BookCertificate()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'store/certificate.html', context)
#

def search(request):
    return render(request, 'store/search.html')
