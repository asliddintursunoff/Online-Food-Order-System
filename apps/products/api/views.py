from rest_framework import views,generics,viewsets,mixins,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser

from apps.products.models import ProductCategory,Product
from apps.products.api.serializers import (
    ProductCategorySerializer,ProductSerializer,ProductCategoryDetailSerializer
)
from apps.products.api.filters import CategoryFilter


class ProductCategoryViewSet(viewsets.GenericViewSet,mixins.UpdateModelMixin):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    lookup_field = "id"
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
        print(obj)
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
    parser_classes = [MultiPartParser,FormParser]
    # filterset_fields = ["category__name"]
    filterset_class = CategoryFilter
    def get_queryset(self):
        queryset = self.queryset

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__name = category)
        return queryset
    
    







#file read how it works
# from drf_spectacular.utils import extend_schema

# @extend_schema(request=serializers.FileRead)
# @api_view(['POST','GET'])
# def read_image(request):
#     if request.method == 'POST':
#         file = serializers.FileRead(data = request.data)
          # file = request.FILES.get("key_name")
#         if not file.is_valid():
#             return Response(file.errors)

#         print(file.validated_data['f'].read())
#         return Response({
#             "validated_data":file.validated_data,
#             "data":file.data,
#             "instance":file.instance

#         })