from django.contrib.gis.db import models
from django_tenants.models import DomainMixin,TenantMixin

class Restaurant(TenantMixin):
    name = models.CharField(max_length=100)
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location = models.PointField(null=True)

    auto_create_schema = True

    def __str__(self):
        return self.name
class RestaurantDomain(DomainMixin):
    pass