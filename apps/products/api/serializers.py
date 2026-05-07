from rest_framework import serializers

from apps.products.models import ProductCategory,Product
from apps.common.choices import MassType

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()

    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.save()
        return instance
    
    

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     image = serializers.ImageField()
#     name = serializers.CharField()
#     description = serializers.CharField(required = False)
#     mass = serializers.DecimalField(max_digits=10,decimal_places=3,required = False)
#     mass_type = serializers.ChoiceField(MassType.choices,required = False)
#     price = serializers.DecimalField(decimal_places=2,max_digits=10)

#     def create(self, validated_data):
#         return Product.objects.create(**validated_data)
    

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(write_only = True,queryset=ProductCategory.objects.all())
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        category = validated_data.pop('category_id')
        
        return Product.objects.create(category=category,**validated_data)
    def update(self, instance, validated_data):
        category = validated_data.pop('category_id')
        instance.category =category
        instance.save()
        return instance        


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["category"]

class ProductCategoryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    products = ProductBaseSerializer(many = True,read_only = True)
