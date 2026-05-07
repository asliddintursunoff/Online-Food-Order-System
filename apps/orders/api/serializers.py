from rest_framework import serializers

from apps.orders.models import Order,OrderItem
from apps.common.choices import OrderStatus
from apps.users.api.serializers import OrderLocationSerializer
from apps.products.api.serializers import ProductBaseSerializer
from apps.products.models import Product

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
    

class OrderItemQuantitySerializer(serializers.ModelSerializer):
    product = ProductBaseSerializer(read_only = True)
    quantity = serializers.IntegerField(min_value=0)
    
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity']
     
    
    
    def update(self, instance, validated_data):
        new_quantity = validated_data.get('quantity',instance.quantity)
        order = instance.order
        old_quantity = instance.quantity

        instance.quantity = new_quantity
        order.total_price -= old_quantity*instance.product.price
        order.total_price += new_quantity*instance.product.price

        instance.save()
        order.save()

        return instance
    


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    location = OrderLocationSerializer(read_only = True)
    
    class Meta:
        model = Order
        fields = '__all__'
    
    

