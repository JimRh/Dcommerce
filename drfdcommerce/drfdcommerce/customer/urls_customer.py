from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register),
    path('login',views.login),
    path('order',views.create_order),
    path('paymentsuccess/<int:userid>/<str:address>/<str:phone>',views.confirm_order)
]