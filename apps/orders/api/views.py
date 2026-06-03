from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status,mixins
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import CanUpdateOrderStatus
from django.utils import timezone

from apps.orders.models import Order
from apps.common.choices import OrderStatus,UserRole
from apps.orders.api.serializers import OrderSerializer, OrderStatusSerializer,OrderListSerializer
from apps.orders.utils import calculating_imaginary_devilery_time


    
class OrderDetailAPIView(GenericViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin
                        ):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.user
        if user.role == UserRole.CLIENT:
            return queryset.filter(user=user)
        return queryset

    
class OrderStatusAPIView(GenericViewSet,mixins.ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [CanUpdateOrderStatus]
    lookup_field = 'id'
    filterset_fields = ['status']
    
    def update(self,request,id):
        order = self.get_object()
        self.check_object_permissions(request, order)
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data["status"]
        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data)
    
    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            self.serializer_class = OrderListSerializer
        return super().get_serializer(*args, **kwargs)
    
    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.user
        if user.role == UserRole.CLIENT:
            queryset = queryset.filter(user=user)

        elif user.role == UserRole.DELIVERER:

            queryset = queryset.filter(
                status__in=[
                    OrderStatus.READY,
                    OrderStatus.DELIVERING
                ]
            )
        stat = self.request.query_params.get("status")

        if stat:
            queryset = queryset.filter(status=stat)

        return queryset.order_by("created_at")
   
class CreateOrderAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        order = serializer.save(
            user=request.user
        )
        data = OrderSerializer(order).data
        count = Order.objects.filter(
            status=OrderStatus.PREPARING
        ).count()
        est_time = calculating_imaginary_devilery_time(count,order.location.point)
        data['delivery_time'] = est_time
        return Response(
            data,
            status=status.HTTP_201_CREATED
        )