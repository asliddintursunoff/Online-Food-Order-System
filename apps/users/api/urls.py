from django.urls import path,include

from rest_framework.routers import DefaultRouter

from apps.users.api import views


router = DefaultRouter()


router.register('location',views.UserLocationAPIView)
router.register('auth',views.UserRegistrationAPIView,basename="user-reg")

router.register('worker',views.AddWorkerAPIView,basename="worker-reg")
urlpatterns = [
    path('',include(router.urls)),
    path('token/',views.MyTokenAPIView.as_view())
   
]