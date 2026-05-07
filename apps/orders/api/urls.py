from django.urls import path,include

from apps.orders.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("status",views.OrderStatusUpdateAPIView,basename="status")
router.register("",views.OrderAPIView)
urlpatterns = [
    path('my-cart',views.MyCartAPIView.as_view()),
    path('items/',views.OrderItemAPIView.as_view()),
    path('items/<int:id>',views.OrderItemDetailAPIView.as_view()),
    path('',include(router.urls)),
    path('<int:id>/',views.get_detail_order)
]