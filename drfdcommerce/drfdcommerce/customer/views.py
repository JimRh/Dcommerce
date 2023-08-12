from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

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
    