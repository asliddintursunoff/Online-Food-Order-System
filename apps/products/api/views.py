from rest_framework import filters, viewsets,mixins,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser

from apps.products.models import ProductCategory,Product
from apps.products.api.serializers import (
    ProductCategorySerializer,ProductSerializer,ProductCategoryDetailSerializer,
    ProductListViewSerializer
)
from apps.products.api.pagination import ProductPagination

from django_filters.rest_framework import DjangoFilterBackend

from apps.common.permissions import IsADMIN
from rest_framework.permissions import AllowAny


class ProductCategoryViewSet(viewsets.GenericViewSet,mixins.UpdateModelMixin):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    lookup_field = "id"

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["create","destroy","update","partial_update"]:
            permissions = [IsADMIN]

        return [permission() for permission in permissions]
    
    def list(self,request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many = True
        )

        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    def destroy(self,request,*args,**kwargs):
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   
    
    #Customizing endpoint and add extra API for you API
    #that returns products related to this object
    @action(detail = True,methods = ['GET'])
    def products(self,request,id):
        obj = self.get_object()
        
        serializer = ProductCategoryDetailSerializer(obj)
        return Response(serializer.data)


class ProductApiView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    parser_classes = [MultiPartParser,FormParser]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ["category__id"]
    search_fields = ["name"]
  
    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = ProductListViewSerializer
        else:
            serializer_class = ProductSerializer
        
       
        return serializer_class(*args, **kwargs)
    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["create","destroy","update","partial_update"]:
            permissions = [IsADMIN]

        return [permission() for permission in permissions]
    
    def get_queryset(self):
        queryset = self.queryset

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__name = category)
        return queryset
    
    
    






