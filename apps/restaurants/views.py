from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django_tenants.utils import schema_context
from django.db import transaction,IntegrityError


from apps.restaurants.models import Restaurant
from apps.restaurants.models import Restaurant,RestaurantDomain
from apps.common.choices import UserRole

from rest_framework import serializers

class RestaurantRegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    address_line = serializers.CharField()
    city = serializers.CharField()
    lat = serializers.DecimalField(max_digits=20, decimal_places=15,write_only = True)
    lon =  serializers.DecimalField(max_digits=20, decimal_places=15,write_only = True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    phone_number = serializers.CharField()



class RestaurantRegister(GenericAPIView):
    
    serializer_class = RestaurantRegisterSerializer
    def post(self,request):
        data = RestaurantRegisterSerializer(data = request.data)
        if not data.is_valid():
            return Response(data.errors)
        try:
            with transaction.atomic():
                restaurant_name = str(data.data.get("name")).lower().replace(" ","-")
                restaurant = Restaurant(name = data.data.get("name"),
                                        address_line = data.data.get("address_line"),
                                        city = data.data.get("city"),
                                        location = Point(data.data.get('lat'),data.data.get('lon')),
                                        schema_name =restaurant_name)
                
                restaurant.save()
                from django.conf import settings
                domain_name = restaurant_name+"."+settings.BASE_DOMAIN
                domain = RestaurantDomain(domain = domain_name,
                                        tenant = restaurant)
                domain.save()

                with schema_context(restaurant.schema_name):
                    from apps.users.models import User
                    user = User(first_name = data.data.get("first_name"),
                                last_name = data.data.get("last_name"),
                                username = data.data.get("username"),
                                phone_number = data.data.get("phone_number"),
                                role = UserRole.ADMIN
                                )
                    user.set_password(data.data.get('password'))
                    user.save()
        
        except IntegrityError as e:
           
            return Response(
                {"error": "Restaurant or username already exists!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {"message":"Restaurant created!",
            "domain": domain.domain}
        )

            





        

