from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from apps.orders.models import Order,OrderItem
from apps.common.choices import OrderStatus
from apps.orders.api.serializers import OrderSerializer,OrderItemSerializer,OrderItemQuantitySerializer


class OrderAPIView(APIView):
    
    def get(self,request):
        user = request.user
        
        pending_order = Order.objects.filter(user = user, status = OrderStatus.PENDING).first()
        if not pending_order:
            pending_order = Order.objects.create(user = user)
        serializer = OrderSerializer(pending_order)
        return Response(serializer.data)
    

class OrderItemAPIView(GenericAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    lookup_field = 'id'
    def post(self,request):
        user = request.user
        pending_order = Order.objects.filter(user = user, status = OrderStatus.PENDING).first()
        if not pending_order:
            pending_order = Order.objects.create(user = user)

        serializer =self.get_serializer(data = request.data)
        
        if not  serializer.is_valid():
            return Response(serializer.errors)
        
        item = OrderItem.objects.create(order = pending_order,
                                 product =serializer.validated_data["product_id"],
                                 quantity = serializer.validated_data["quantity"])
        pending_order.total_price += item.product.price*item.quantity
        pending_order.save()
        return Response(self.get_serializer(item).data)
    


class OrderItemDetailAPIView(GenericAPIView):
    serializer_class = OrderItemQuantitySerializer
    queryset = OrderItem.objects.all()
    lookup_field = 'id'

    def delete(self,request,id):
        obj = self.get_object()

        order = obj.order
        order.total_price -= obj.product.price*obj.quantity
        obj.delete()
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    def put(self,request,id):
        obj = self.get_object()
        serializer = self.get_serializer(obj,data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)


        serializer.save()
        if serializer.validated_data.get('quantity') == 0:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)

        