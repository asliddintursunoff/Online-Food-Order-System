from django.urls import path,include

from apps.orders.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("status",views.OrderStatusAPIView,basename="status")
# router.register("",views.OrderStatusAPIView)
router.register('detail',views.OrderDetailAPIView,basename="detail")
urlpatterns = [
    # path('my-cart',views.MyCartAPIView.as_view()),
    path('',views.CreateOrderAPIView.as_view()),
    # path('items/<int:id>',views.OrderItemDetailAPIView.as_view()),
    path('',include(router.urls)),
    
]

