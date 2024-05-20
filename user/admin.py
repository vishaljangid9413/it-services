from django.contrib import admin
from .models import  *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'mobile','is_active',)
