from rest_framework import serializers

from apps.users.models import UserLocation


class OrderLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['address_line','city']