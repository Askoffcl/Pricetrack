from django.db import models
from users.models import Register

class Product(models.Model):
    shopid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productname = models.CharField(max_length=20)
    productcate = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/',null=True)


class Order(models.Model):
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    orderdate = models.DateTimeField(auto_now_add=True)
 
class Feedback(models.Model):
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(null=True)
    comment = models.CharField(max_length=200,null=True)


class Complaint(models.Model):
    CHOICES = [
        ('pending', 'Pending'),
        ('working on', 'Working on'),
        ('resolved', 'Resolved')
    ]
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name='user_complaint')
    description = models.TextField(max_length=200,null=True)
    status = models.CharField(max_length=20,choices=CHOICES,default='pending',null=True)

