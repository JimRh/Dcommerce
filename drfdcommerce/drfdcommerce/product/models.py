from django.db import models
from mptt.models import MPTTModel,TreeForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Category(MPTTModel):

    name=models.CharField(max_length=100)
    parent=TreeForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    
    class MPPTMeta:
        order_insertion_by=['name']

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=100)
    quantity= models.IntegerField()
    price=models.IntegerField()
    description=models.TextField(blank=True)
    category = TreeForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

class CartItems(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    itemprice=models.IntegerField()
    item_totalprice=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

