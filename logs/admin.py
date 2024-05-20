from django.contrib import admin
from .models import OTPLog


@admin.register(OTPLog)
class OTPLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'purpose', 'status', 'created_at')


