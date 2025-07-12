from django.db import models
from . managers import UserManager
from django.contrib.auth.models import AbstractUser , AbstractBaseUser
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here.



class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11 , unique=True , verbose_name="Phone number")
    email = models.EmailField(max_length=100,unique=True,verbose_name="Email adress")
    date_joined = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["email",]
    USERNAME_FIELD = "phone_number"


    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    



class OtpCode(models.Model):
    code = models.SmallIntegerField(validators=[MinValueValidator(1000),MaxValueValidator(9999)])
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.code}"

    def is_expired(self):
        return (timezone.now() - self.created) > timedelta(minutes=3)


    class Meta:
        ordering = ("-created",)
