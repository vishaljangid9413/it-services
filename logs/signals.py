# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import OTPLog

@receiver(post_save, sender=OTPLog)
def expire_old_otps(sender, instance, **kwargs):
    expiration_time = timezone.now() - timedelta(minutes=5)
    OTPLog.objects.filter(status='generated', created_at__lt=expiration_time).update(status='expired')
