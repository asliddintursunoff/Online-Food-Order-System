from django.contrib.gis.db import models

from django.contrib.auth.models import AbstractUser

from apps.common.choices import UserRole

class User(AbstractUser):
    username = None
    phone_number = models.CharField(db_index=True,unique=True,max_length=13,null=True,blank=True)
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        max_length=20
    )

    USERNAME_FIELD = 'phone_number'

class UserLocation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    point = models.PointField(null=True)

