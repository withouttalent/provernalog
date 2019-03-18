from django.urls import path, include
from .views import *

urlpatterns = [
    path('capture/', capture, name='capture'),
    path('products/<str:product_id>/', order, name='order'),
    path('products/', index, name='index')
]
