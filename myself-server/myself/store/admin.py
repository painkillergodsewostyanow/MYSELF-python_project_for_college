from django.contrib import admin
from django.utils.safestring import mark_safe
from store.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'get_image')
    search_fields = ('title',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="70">')

    get_image.short_description = "Миниатюра"



