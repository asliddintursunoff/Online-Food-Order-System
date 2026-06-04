from rest_framework import serializers

from apps.common.choices import UserRole
from apps.users.models import UserLocation,User
from django.contrib.gis.geos import Point
import re
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenSerializer(TokenObtainPairSerializer):
    username_field = 'phone_number'
    def validate(self, attrs):
        result =  super().validate(attrs)
        result['role'] = self.user.role

        return result
    

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "id","first_name","last_name","password","password_confirm","phone_number","role"
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            },

            "role": {
                "read_only": True
            }
        }

    def validate_phone_number(self, value):
        pattern = r'^\+998(90|91|93|94|95|97|98|99|33|88|77)\d{7}$'
        
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Phone number must start with +998 followed by valid operator code. Example: +998901234567"
            )
        
        return value

    def validate(self, attrs):

        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm", None)

        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match."
            })

        if len(password) < 8:
            raise serializers.ValidationError({
                "password": "Password must be at least 8 characters."
            })
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        new_user = User(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user
    
class WorkerADDSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):

        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "role": {
                "read_only": False
            }
        }

    def validate_role(self, value):
        allowed_roles = [
            UserRole.WAITER,
            UserRole.DELIVERER,
            UserRole.ADMIN
        ]

        if value not in allowed_roles:
            raise serializers.ValidationError(
                "Only worker roles are allowed."
            )

        return value
    
class OrderLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['address_line','city']


class OrderLocationDetailSerializer(OrderLocationSerializer):
    latitude = serializers.DecimalField(max_digits=20, decimal_places=15,write_only = True)
    longitude = serializers.DecimalField(max_digits=20, decimal_places=15,write_only = True)
    class Meta:
        model = UserLocation
        exclude = ["point"]
        extra_kwargs = {
            "user":{"read_only":True},
        
        }

    def create(self, validated_data):
        lat = float(validated_data.pop('latitude'))
        lon = float(validated_data.pop('longitude'))

        point = Point(lon, lat, srid=4326)

        return UserLocation.objects.create(
            **validated_data,
            point=point
        )