from rest_framework import serializers
from .models import *
from ..product.models import Product
from ..product.serializers import ProductSerializers


class OrderSerialziers(serializers.ModelSerializer):

    class Meta:
        model=Order

        fields='__all__'

class OrderItemsSerializers(serializers.ModelSerializer):

    order=OrderSerialziers()
    product=ProductSerializers()

    class Meta:

        model=OrderItems
        fields=['product','price','quantity','order']




    
