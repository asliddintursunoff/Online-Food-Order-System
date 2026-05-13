from rest_framework import viewsets,mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.api.permissions import IsSelfOrAdmin
from apps.users.models import UserLocation,User
from apps.users.api.serializers import OrderLocationDetailSerializer,UserSerializer,WorkerADDSerializer,MyTokenSerializer
from apps.common.permissions import IsADMIN


from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenAPIView(TokenObtainPairView):
    serializer_class = MyTokenSerializer

    
class UserLocationAPIView(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin):
    
    queryset = UserLocation.objects.all()
    serializer_class = OrderLocationDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    def get_queryset(self):
        return UserLocation.objects.filter(user = self.request.user)
    


class UserRegistrationAPIView(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsSelfOrAdmin()]


class AddWorkerAPIView(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = WorkerADDSerializer
    permission_classes = [IsADMIN]

    