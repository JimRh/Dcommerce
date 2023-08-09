from django.db import models
from mptt.models import MPTTModel,TreeForeignKey
# Create your models here.

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
