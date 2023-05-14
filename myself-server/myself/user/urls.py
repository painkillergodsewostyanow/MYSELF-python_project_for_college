from .views import *
from django.urls import path


app_name = 'user'

urlpatterns = [
    path('reg', reg, name='reg'),
    path('log', log, name='log'),
    path('logout', logout, name='logout'),
    path('favorite', favorite, name='favorite'),
    path('profile', profile, name='profile')
]
