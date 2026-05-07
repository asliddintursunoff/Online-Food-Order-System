from django.urls import include,path

from rest_framework.routers import DefaultRouter

from apps.restaurants.api import views


router = DefaultRouter()

router.register('',views.RestaurantViewSet,basename="restaurant")

urlpatterns = [
    path("",include(router.urls)),
]