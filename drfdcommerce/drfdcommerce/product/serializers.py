from rest_framework import serializers
from .models import Category,Product


class CategorySerializers(serializers.ModelSerializer):
    
    parent=serializers.ReadOnlyField(source='parent.name',read_only=True)
    
    
    class Meta:
        model=Category
        fields=['name','parent']
  


class ProductSerializers(serializers.ModelSerializer):
    
    category=CategorySerializers()

    class Meta:
        model=Product
        fields=['id','name','description','quantity','price','category']


       




