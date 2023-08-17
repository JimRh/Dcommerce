
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import CategorySerializers,ProductSerializers,CartItemSerializers,CartSerializers
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

@api_view(['POST'])

def add_cartitems(request):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    if request.method=="POST":
        
        if request.user.is_authenticated:
            user=request.user
            user_id = request.user.id
            product_id=request.data['product_id']
            product_id=int(product_id)
            product_quantity=request.data['quantity']
            product=Product.objects.get(id=product_id)
            
           
            
            price=product.price
            items_totalprice=product_quantity*price
            
            
            
            cart,_=Cart.objects.get_or_create(customer=user)
            
            cart_item = CartItems.objects.create(
            customer=user,
            cart=cart,
            product=product,
            quantity=product_quantity,
            itemprice=price,
            item_totalprice=items_totalprice
            )
            


        
        
            cartdata=Cart.objects.filter(customer=user_id)
            
            totalprice=0
            if cartdata[0].total_price is None:
                totalprice=0
            else:
                totalprice=cartdata[0].total_price
            
            
            totalprice+=items_totalprice
           
                
            cart.total_price=totalprice
          
            cart.save()
            
            
            return Response(totalprice)
            
            



@api_view(['POST'])

def remove_cartitem(request):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    if request.user.is_authenticated:
        user=request.user
        user_id = request.user.id
        print(user_id)
        product_id=request.data['product_id']
        caritems=CartItems.objects.get(product_id=product_id,customer_id=user_id)
        cart=Cart.objects.get(customer=user_id)
        cartprice=cart.total_price
        updated_price=0
        if caritems:
            price=caritems.item_totalprice
            updated_price=cartprice-price
            caritems.delete()
        cart.total_price=updated_price
        cart.save()
        return Response("Item removed")
            

@api_view(["GET"])

def get_cartitems(request):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    if request.user.is_authenticated:
        user_id=request.user.id
        query=CartItems.objects.filter(customer=user_id)
        
        cart=CartItemSerializers(query,many=True)
        
        return Response(cart.data)



