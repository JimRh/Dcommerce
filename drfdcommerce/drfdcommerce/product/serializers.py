from rest_framework import serializers
from .models import Category,Product


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=['name']
  


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=['name','description','quantity','price']




