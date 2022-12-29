from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

admin.site.register(OrderItem)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter=['created_at', 'updated_at', 'status']