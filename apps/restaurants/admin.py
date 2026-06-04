from django.contrib import admin
from apps.restaurants.models import RestaurantDomain,Restaurant

admin.site.register(Restaurant)
admin.site.register(RestaurantDomain)
