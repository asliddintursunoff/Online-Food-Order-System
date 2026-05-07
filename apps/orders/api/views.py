from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.decorators import action,api_view

from django.shortcuts import get_object_or_404

from apps.orders.models import Order,OrderItem
from apps.common.choices import OrderStatus
from apps.orders.api.serializers import OrderSerializer,OrderItemSerializer,OrderItemQuantitySerializer
from django.utils import timezone




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


#
class MyCartAPIView(APIView):
    def get(self,request):
        user = request.user
        pending_order = Order.objects.filter(user = user, status = OrderStatus.PENDING).first()
        if not pending_order:
            pending_order = Order.objects.create(user = user)
        serializer = OrderSerializer(pending_order)
        return Response(serializer.data)
     
#detail API view

@api_view(["GET"])
def get_detail_order(request,id):
    try:
        order = get_object_or_404(Order,id=id)
        
        serializer = OrderSerializer(order)

        return Response(serializer.data)
    except Order.DoesNotExist as e:
        return Response({"detail":str(e)},status=status.HTTP_404_NOT_FOUND)
class OrderStatusUpdateAPIView(GenericViewSet):
    queryset = Order.objects.all()
    lookup_field = 'id'
   
    @action(detail=True,methods=['post'])
    def cancel(self,request,id):
        order = self.get_object()
        order.status = OrderStatus.CANCELED
        order.canceled_at = timezone.now()
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def confirmed(self,request,id):
        order = self.get_object()
        #I used agregation for counting items
        if order.order_items.count() == 0:
            return Response({"detail":"No items selected"},status=status.HTTP_400_BAD_REQUEST)
        
        if order.location is None:
            return Response({"detail":"No location found"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order.status = OrderStatus.CONFIRMED
        order.created_at = timezone.now()
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
   
    @action(detail=True,methods=['post'])
    def preparing(self,request,id):
        order = self.get_object()
        order.status = OrderStatus.PREPARING
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def ready(self,request,id):
        order = self.get_object()
        order.status = OrderStatus.READY
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def delivering(self,request,id):
        order = self.get_object()
        order.status = OrderStatus.DELIVERING
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def done(self,request,id):
        order = self.get_object()
        order.status = OrderStatus.DONE
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    

class OrderAPIView(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False,methods=['GET'])
    def new_orders(self,request):
        queryset = Order.objects.filter(status = OrderStatus.CONFIRMED).order_by("created_at")
        serializer = self.get_serializer(queryset,many=True)


        return Response(serializer.data)

    @action(detail=False,methods=['GET'])
    def preparing(self,request):
        queryset = Order.objects.filter(status = OrderStatus.PREPARING).order_by("created_at")
        serializer = self.get_serializer(queryset,many=True)

    
        return Response(serializer.data)

    @action(detail=False,methods=['GET'])
    def ready(self,request):
        queryset = Order.objects.filter(status = OrderStatus.READY).order_by("created_at")
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=['GET'])
    def delivering(self,request):
        queryset = Order.objects.filter(status = OrderStatus.DELIVERING).order_by("created_at")
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=['GET'])
    def done(self,request):
        queryset = Order.objects.filter(status = OrderStatus.DONE).order_by("created_at","delivered_at")
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=['GET'])
    def canceled(self,request):
        queryset = Order.objects.filter(status = OrderStatus.CANCELED).order_by("created_at","canceled_at")
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    

   
