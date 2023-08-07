
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category,Product
from .serializers import CategorySerializers,ProductSerializers
# Create your views here.

@api_view(['GET'])

def get_category(request):
    if request.method=="GET":
        queryset=Category.objects.all()
        category=CategorySerializers(queryset,many=True)
        return Response(category.data)


