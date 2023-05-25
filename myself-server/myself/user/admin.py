from django.contrib import admin
from user.models import User, Favorite


class FavoriteAdmin(admin.TabularInline):
    model = Favorite
    fields = ('product', 'quantity', 'create_timestamp')
    readonly_fields = ('create_timestamp', )
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (FavoriteAdmin, )
