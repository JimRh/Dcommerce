
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import CategorySerializers,ProductSerializers
# Create your views here.

@api_view(['GET'])

def get_category(request):
    if request.method=="GET":
        queryset=Category.objects.all()
        category=CategorySerializers(queryset,many=True)
        return Response(category.data)


@api_view(['GET'])

def get_product(request):
    if request.method=="GET":
        queryset=Product.objects.all()
        product=ProductSerializers(queryset,many=True)
        return Response(product.data)

@api_view(['GET'])

def get_product_by_cat(request,category):
    if request.method=="GET":
        category=Category.objects.get(name=category)
        subcategory=category.get_descendants(include_self=True)
        queryset=Product.objects.filter(category__in=subcategory)
        product=ProductSerializers(queryset,many=True)
        return Response(product.data)

