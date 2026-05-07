from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.choices import UserRole

class User(AbstractUser):
    phone_number = models.CharField(max_length=13,null=True,blank=True)
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        max_length=20
    )

class UserLocation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
    

