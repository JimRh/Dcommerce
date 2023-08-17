from rest_framework import serializers
from .models import Category,Product,Cart,CartItems


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


       
class CartSerializers(serializers.ModelSerializer):

    class Meta:
        model=Cart
        fields=['total_price']


class CartItemSerializers(serializers.ModelSerializer):
    product=ProductSerializers()
    cart=CartSerializers()
    
    class Meta:
        model=CartItems
        fields=['product','quantity','itemprice','item_totalprice','cart']

