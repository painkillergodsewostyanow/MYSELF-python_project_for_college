from .views import *
from django.urls import path


app_name = 'user'

urlpatterns = [
    path('reg', reg, name='reg'),
    path('log', log, name='log'),
    path('logout', logout, name='logout'),
    path('favorite', show_favorite, name='favorite'),
    path('profile', profile, name='profile'),
    path('favorite/add/<int:product_id>/', add_to_favorite, name="add_to_favorite"),
    path('favorite/del/<int:favorite_id>/', del_from_favorite, name="del_from_favorite")
]
