from django.contrib import admin
from .models import  *

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'tax', 'package')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'payment_status', 'amount', 'date')
