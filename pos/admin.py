from django.contrib import admin

# Register your models here.

from .models import Product, Purchase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'available_quantity', 'description')
    search_fields = ('name', 'description')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')
    search_fields = ('product',)


