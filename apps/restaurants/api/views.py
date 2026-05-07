from rest_framework import generics,viewsets


from apps.restaurants.api.serializers import RestaurantSerializer
from apps.restaurants.models import Restaurant


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    
