from django.db import models
from django.contrib.auth.models import User
from ..product.models import Product
# Create your models here.
class Order(models.Model):
    
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_address=models.CharField(max_length=200)
    payment_status=models.BooleanField(default=False)
    contact_number=models.CharField(max_length=11)
    total_order_price=models.IntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):

    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    quantity=models.IntegerField()

