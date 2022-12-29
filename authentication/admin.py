from django.contrib import admin
from .models import User, PhoneNumber, Address

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined','is_active', 'is_staff' ] 

admin.site.register(PhoneNumber)
admin.site.register(Address)
