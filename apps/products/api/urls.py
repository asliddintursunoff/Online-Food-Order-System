from django.urls import path,include
from rest_framework.routers import DefaultRouter

from apps.products.api import views

router = DefaultRouter()

router.register("category",views.ProductCategoryViewSet,basename="category")
router.register("products",views.ProductApiView,basename="products")

urlpatterns = [
    path('',include(router.urls)),
    
]