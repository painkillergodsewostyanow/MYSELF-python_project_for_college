from django.contrib import admin
from store.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'size', 'quantity_in_stock', 'get_image')
    search_fields = ('title', 'size')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="70">')

    get_image.short_description = "Миниатюра"


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_recipient', 'value', 'name_payer', 'phone_number_payer', 'is_used')
    search_fields = ('name_recipient', 'size')


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Size)
