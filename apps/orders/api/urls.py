from django.urls import path

from apps.orders.api import views

urlpatterns = [
    path('current',views.OrderAPIView.as_view()),
    path('items/',views.OrderItemAPIView.as_view()),
    path('items/<int:id>',views.OrderItemDetailAPIView.as_view())
]