import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import *
from .manager import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    fullname = CharField(max_length=100)
    email = EmailField()
    mobile = CharField(max_length=15, unique=True)
    address = TextField()
    registration_datetime = DateTimeField(auto_now_add=True,null=True, blank=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_deleted = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["fullname", 'email']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email