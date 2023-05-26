from django.contrib.auth.views import LogoutView
from .views import *
from store.views import *
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('reg', UserRegistrationView.as_view(), name='reg'),
    path('log', UserLoginView.as_view(), name='log'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('favorite', FavoriteListView.as_view(), name='favorite'),
    path('profile', profile, name='profile'),
    path('favorite/add/<int:product_id>/', add_to_favorite, name="add_to_favorite"),
    path('favorite/del/<int:favorite_id>/', del_from_favorite, name="del_from_favorite")
]
