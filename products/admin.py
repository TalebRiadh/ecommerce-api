from django.contrib import admin
from lib import custom_titled_filter
from .models import Product, ProductCategory
# Register your models here.
admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter=(
        ('created_at', custom_titled_filter('Created At')),
        ('updated_at', custom_titled_filter('Updated At')),
        )