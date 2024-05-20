from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,fullname, email, mobile, password, **extra_fields):
        if not email and not mobile:
            raise ValueError("At least one of email or mobile must be set.")
        
        if not fullname:
            raise ValueError("name must be set.")
        
        if email:
            email = self.normalize_email(email)

        user = self.model(fullname=fullname, email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, mobile, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(fullname, email, mobile, password, **extra_fields)


        