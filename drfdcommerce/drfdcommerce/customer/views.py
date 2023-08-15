from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..product.models import CartItems,Cart
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order,OrderItems


@api_view(['POST'])

def register(request):

        try:
            username=request.data['username']
            email=request.data['email']
            first_name=request.data['first_name']
            last_name=request.data['last_name']
            password1=request.data['password']
            

            if User.objects.filter(email=email).exists():
                return Response({"error":"emailexists"})
            user=User()
            user.username=username
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            user.is_active=True
            user.set_password(raw_password=password1)
            user.save()
            return Response({"Success":"User has been created"})
        except:
            return Response({"Error":"Something went wrong"})
        

@api_view(['POST'])

def login(request):
    
    username=request.data['username']
    password=request.data['password']

    user=authenticate(username=username,password=password)

    if user is None:
         return Response(
              {
                   "Success":False,
                   "Message":"Invalid Username or Password"
              }
         )
    refresh = RefreshToken.for_user(user)
    return Response(
         {
            "Success":True,
            "Message":{"refresh": str(refresh),
            'access': str(refresh.access_token),
            }
    }
              )        


@api_view(['POST'])

def create_order(request):
     authentication_classes=[JWTAuthentication]
     permission_classes=[IsAuthenticated]
     if request.method=="POST":
        
        if request.user.is_authenticated:
            user=request.user
            user_id = request.user.id
            shipping_address=request.data['address']
            contact_number=request.data['phonenumber']
          
            order,_=Order.objects.get_or_create(customer=user,shipping_address=shipping_address,contact_number=contact_number)
            
            cartitems=CartItems.objects.filter(customer=user_id)
            cart=Cart.objects.get(customer=user_id)
            total_price=cart.total_price
            for item in cartitems:
                 product_id=item.product.id
                 product=item.product 
                 price=item.itemprice
                 quantity=item.quantity
                 
                 OrderItems.objects.create(
                      customer=user,
                      order=order,
                      price=price,
                      product=product,
                      quantity=quantity
                      )

        order.total_order_price=total_price
        order.save()
            
     return Response("ok")
            
    