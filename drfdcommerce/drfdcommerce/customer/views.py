from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..product.models import Product,CartItems,Cart
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order,OrderItems
from .onlinepayment import make_payment
from .serializers import OrderItemsSerializers
import uuid
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
     flag=False
     if request.method=="POST":
        
        if request.user.is_authenticated:
            user=request.user
            userid = request.user.id
            
            shipping_address=request.data['address']
            contact_number=request.data['phonenumber']
            payment_method=request.data['payment_method'] 
            cartitems=CartItems.objects.filter(customer=userid)
            cart=Cart.objects.get(customer=userid)
            total_price=cart.total_price
            
            if payment_method=='COD':
               order=Order.objects.create(customer=user)
               for item in cartitems:
                   product_id=item.product.id
                   quantity=item.quantity
                   price=item.item_totalprice
                   product=Product.objects.get(id=product_id)
                   cur_quanity=product.quantity
                   if cur_quanity>=quantity:
                         OrderItems.objects.create(
                                   customer=user,
                                   order=order,
                                   price=price,
                                   product=product,
                                   quantity=quantity
                                   )
                         updated_quantity=cur_quanity-quantity
                         product.quantity=updated_quantity
                         product.save()
                         flag=True     
                   else:
                       flag=False
               if flag:          
                    order.shipping_address=shipping_address
                    order.contact_number=contact_number
                    order.total_order_price=total_price
                    order.save()
                    cart.delete()
                    return Response("ok")
               else:
                   order.delete()
                   return Response("Quntity is more than stock")
               
                        
                         

               
               

            else:
               username="test"
               tran_id=uuid.uuid4()
               response=make_payment(total_price,tran_id,username,userid,shipping_address,contact_number)
               redirect_url=response['redirectGatewayURL']
              
               
              
               return Response(redirect_url)
               
             
     
@api_view(['POST'])
def confirm_order(request,userid,address,phone):
    flag=False
    if request.method=="POST":
        
        user=User.objects.get(id=userid)
        print(user)
        order=Order.objects.create(customer=user)
            
        cartitems=CartItems.objects.filter(customer=userid)
        cart=Cart.objects.get(customer=userid)
        total_price=cart.total_price
        for item in cartitems:
               product_id=item.product.id
               quantity=item.quantity
               price=item.item_totalprice
               product=Product.objects.get(id=product_id)
               cur_quanity=product.quantity
               if cur_quanity>=quantity:
                         print('yes')
                         OrderItems.objects.create(
                                   customer=user,
                                   order=order,
                                   price=price,
                                   product=product,
                                   quantity=quantity
                                   )
                         updated_quantity=cur_quanity-quantity
                         product.quantity=updated_quantity
                         product.save()
                         flag=True     
               else:
                    flag=False
        if flag:          
                order.shipping_address=address
                order.contact_number=phone
                order.payment_status=True
                order.total_order_price=total_price
                order.save()
                cart.delete()
                return Response("ok")
        else:
            order.delete()
            return Response("Quntity is more than stock")
    

@api_view(["GET"])

def get_orders(request):
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    if request.user.is_authenticated:
        user_id=request.user.id
        orders=Order.objects.filter(customer=user_id)
        
        orderlist=[]

        for order in orders:
             orderitemslist=[]
             orderdic={}
             id=order.id
             
             payment_status=order.payment_status
             order_total_price=order.total_order_price
             order_date=order.created_at
             
             orderitems=OrderItems.objects.filter(order_id=id)
             
             for items in orderitems:
                  orderitemsdata={
                       
                       "product_id":items.product.id,
                       "product_name":items.product.name,
                       "product_quantity":items.quantity,
                       "product_price":items.product.price,
                     


                  }
                  orderitemslist.append(orderitemsdata)
                  
             orderdic={'orderid':id,'orderitems':orderitemslist,'payment_status':payment_status,'order_price':order_total_price,'order_date':order_date}
             orderlist.append(orderdic)     
                 
             
             

        
        
        return Response(orderlist)
    
