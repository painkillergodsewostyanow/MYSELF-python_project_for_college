from django.contrib import admin
from user.models import User, Favorite, Certificate, Basket


class FavoriteAdmin(admin.TabularInline):
    model = Favorite
    fields = ('product', 'create_timestamp')
    readonly_fields = ('create_timestamp', )
    extra = 0


class CertificateAdmin(admin.TabularInline):
    model = Certificate
    fields = ('value', 'is_used')
    readonly_fields = ('user', 'value')
    extra = 0


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (FavoriteAdmin, CertificateAdmin, BasketAdmin)



