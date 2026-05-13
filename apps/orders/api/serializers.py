from rest_framework import serializers

from apps.orders.models import Order,OrderItem
from apps.common.choices import OrderStatus
from apps.users.api.serializers import OrderLocationSerializer,UserSerializer
from apps.products.api.serializers import ProductBaseSerializer
from apps.products.models import Product
from apps.users.models import UserLocation
from django.utils import timezone
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductBaseSerializer(read_only = True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),write_only = True
    )
    quantity = serializers.IntegerField(min_value=0)
    class Meta:
        model = OrderItem
        fields = ['id','product_id','product','quantity']
    
    def create(self, validated_data):
        product = validated_data.pop("product_id")
        return OrderItem.objects.create(**validated_data,product = product)
    




class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    location = OrderLocationSerializer(read_only = True)
    location_id = serializers.PrimaryKeyRelatedField(queryset = UserLocation.objects.all(),write_only = True,required = True)
    user = UserSerializer(read_only = True)
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            "id":{"read_only":True},
            "created_at":{"read_only":True},
            "delivered_at":{"read_only":True},
            "canceled_at":{"read_only":True},
            "status":{"read_only":True},
            "total_price":{"read_only":True},
        }

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        location = validated_data.pop("location_id")

        order = Order.objects.create(
            location=location,
            status=OrderStatus.PENDING,
            **validated_data
        )

        total_price = 0

        for item_data in order_items_data:
            product = item_data.pop("product_id")

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data["quantity"]
            )

            total_price += (
                order_item.product.price *
                order_item.quantity
            )

        order.total_price = total_price
  
        order.save()

        return order
    
    def update(self, instance, validated_data):
        location = validated_data.get("location_id",instance.location)
        instance.location = location
        instance.created_at = validated_data.get("created_at",instance.created_at)
        instance.delivered_at = validated_data.get("delivered_at",instance.delivered_at)
        instance.canceled_at = validated_data.get("canceled_at",instance.canceled_at)
        instance.status = validated_data.get("status",instance.status)
        instance.total_price = validated_data.get("total_price",instance.total_price)
        instance.save()
        return instance

    

class OrderStatusSerializer(serializers.Serializer):
  
    status = serializers.ChoiceField(
        choices=OrderStatus.choices
    )
    


