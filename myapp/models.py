from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class customuser(AbstractUser):
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    city = models.CharField(max_length=100)
