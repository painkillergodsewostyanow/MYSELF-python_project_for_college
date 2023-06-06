from django.contrib import admin
from store.models import *


def make_copy(modeladmin, request, queryset):
    print(queryset)
    for ad in queryset:
        ad.pk = None
        ad.save()


make_copy.short_description = "Дублировать объект"


class PhotoImagesInline(admin.TabularInline):
    model = ProductImages.product.through
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'size', 'quantity_in_stock', 'color', 'get_image')
    search_fields = ('title', 'size')
    inlines = (PhotoImagesInline, )
    actions = (make_copy,)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="70">')

    get_image.short_description = "Миниатюра"


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductImages)
admin.site.register(Color)
admin.site.register(Size)


