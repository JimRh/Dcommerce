from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/category',views.get_category),
    path('api/v1/product',views.get_product),
    path('api/v1/prod_by_cat/<str:category>',views.get_product_by_cat),
    path('api/v1/cart',views.add_cartitems),
]