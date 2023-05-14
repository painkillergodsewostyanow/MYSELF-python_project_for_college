from .views import *
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('reg', reg, name='reg'),
    path('log', log, name='log')
]
