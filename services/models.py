from django.db import models

# Create your models here.
class Service(models.Model):
    PACKAGES = [
        ('free', 'Free'),
        ('paid', 'Paid')
    ]
    name = models.CharField(max_length=50)
    payment_terms = models.TextField()
    price = models.IntegerField()
    package = models.CharField(max_length=50, choices = PACKAGES, default="free", blank=True)
    tax = models.FloatField()
    image = models.ImageField(upload_to='services/')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"  


# Create your models here.
class Subscription(models.Model):
    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="subscriptions")
    razorpay_payment_id = models.CharField(max_length=250, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=250, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=250, null=True, blank=True)
    payment_status = models.CharField(max_length=250, default="Pending")
    amount = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"  




  