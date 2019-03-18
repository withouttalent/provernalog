from django.contrib import admin
from .models import Order, Product
# Register your models here.


@admin.register(Order)
class OrderAdminDisplay(admin.ModelAdmin):
    list_display = ('user', 'email', 'status', 'payment_id', 'good')
    date_hierarchy = 'date_created'


@admin.register(Product)
class ProductAdminDisplay(admin.ModelAdmin):
    list_display = ('title', 'price', 'date_created')
    date_hierarchy = 'date_created'
