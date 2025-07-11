from django.db import models
from django.contrib.auth.models import AbstractUser


class Register(AbstractUser):
    name=models.CharField(max_length=40,null=True)
    address=models.CharField(max_length=200,null=True)
    phone=models.IntegerField(null=True)
    approved=models.BooleanField(default=False)
    shopname=models.CharField(max_length=20,null=True)
    licensenumber=models.IntegerField(null=True)
    image=models.ImageField(upload_to='image/',null=True)
    district=models.CharField(max_length=100,null=True)
    place=models.CharField(max_length=255,null=True)
    role=models.CharField(max_length=20,default="admin")

