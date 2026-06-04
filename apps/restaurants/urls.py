from django.urls import path

from apps.restaurants.views import RestaurantRegister

urlpatterns = [
    path('register',RestaurantRegister.as_view()),
]