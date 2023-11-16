from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class customuser(AbstractUser):
    # friends = models.ManyToManyField('self', blank=True)
    is_talking = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    city = models.CharField(max_length=100)
    #add a camera field here 

class waiting_users(models.Model):
    username = models.CharField(max_length=100000)

class UserCommunication(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    offer = models.JSONField(null=True, blank=True)
    answer = models.JSONField(null=True, blank=True)
    d = models.CharField(max_length=100, null=True, blank=True)