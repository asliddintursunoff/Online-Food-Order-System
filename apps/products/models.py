from django.db import models

from apps.common.choices import MassType
class ProductCategory(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name='products')
    image = models.ImageField(upload_to='products/')
    name  = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True)
    mass = models.DecimalField(max_digits=10,decimal_places=3,null=True)
    mass_type = models.CharField(
        choices=MassType.choices,
        null=True
    )
    price = models.DecimalField(decimal_places=2,max_digits=10)
