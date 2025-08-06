from django.db import models
from users.models import Register

class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    shopid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productname = models.CharField(max_length=20)
    productcate = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    brand = models.CharField(max_length=20)
    price = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/',null=True)

class shopProduct(models.Model):
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    shopid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productname = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    price = models.IntegerField(null=True)
    model = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product/',null=True)
    req = models.CharField(max_length=200,default=False)
    quantityAvailable = models.IntegerField(default=0)
    productcate = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    


 
class Feedback(models.Model):
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(shopProduct,on_delete=models.CASCADE,null=True)
    orderid = models.ForeignKey('products.Order',on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(null=True)
    comment = models.CharField(max_length=200,null=True)
    orderdate = models.DateTimeField(auto_now_add=True)

class Complaint(models.Model):
    CHOICES = [
        ('pending', 'Pending'),
        ('working on', 'Working on'),
        ('resolved', 'Resolved')
    ]
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name='user_complaint')
    description = models.TextField(max_length=200,null=True)
    status = models.CharField(max_length=20,choices=CHOICES,default='pending',null=True)
    orderdate = models.DateTimeField(auto_now_add=True)
    reason  = models.TextField(max_length=200,null=True)

class Order(models.Model):
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(shopProduct,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    orderdate = models.DateTimeField(auto_now_add=True)
    pid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    fed = models.IntegerField(default = 1)

class Available(models.Model):
    CHOICES = [
        ('ADDED', 'ADDED'),
        ('Not Added', 'Not Added')
    ]
    shopid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    productname = models.CharField(max_length=20)
    productcate = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    brand = models.CharField(max_length=20)
    price = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/',null=True)
    status = models.CharField(max_length=20,choices=CHOICES,default='Not Added',null=True)
    orderdate = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    productid = models.ForeignKey(shopProduct,on_delete=models.CASCADE,null=True)
    shopid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    quantityAvailable = models.IntegerField(default=0)

class Payment(models.Model):
    name =  models.CharField(max_length=200,null=True)
    cardnumber = models.IntegerField(null = True)
    cvv = models.IntegerField(null =True)
    orderdate = models.DateTimeField(null= True)
    method = models.CharField(max_length=200,null=True)
    orderid = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    productid = models.ForeignKey(shopProduct,on_delete=models.CASCADE,null=True)
