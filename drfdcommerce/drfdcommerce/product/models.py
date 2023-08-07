from django.db import models

# Create your models here.

class Category(models.Model):

    name=models.CharField(max_length=100)
    parent=models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=100)
    quantity= models.IntegerField()
    price=models.IntegerField()
    description=models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
