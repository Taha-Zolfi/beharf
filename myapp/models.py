from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# مدل کاربر سفارشی
class customuser(AbstractUser):
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    city = models.CharField(max_length=100)

class friendship(models.Model):
    sender = models.ForeignKey(customuser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(customuser, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} => {self.receiver} ({self.status})"


class waiting_users(models.Model):
    username = models.CharField(max_length=100000)

class UserCommunication(models.Model):
    offer = models.JSONField(null=True, blank=True)
    answer = models.JSONField(null=True, blank=True)
    d = models.CharField(max_length=100, null=True, blank=True)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

        
class waiting_users_text(models.Model):
    username = models.CharField(max_length=100000)

class UserCommunication_text(models.Model):
    offer = models.JSONField(null=True, blank=True)
    answer = models.JSONField(null=True, blank=True)
    d = models.CharField(max_length=100, null=True, blank=True)
    ice_candidate = models.JSONField(null=True, blank=True)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class waiting_users_test(models.Model):
    username = models.CharField(max_length=100000)
    peer_id = models.CharField(max_length=100000)

class waiting_users_test_video(models.Model):
    username = models.CharField(max_length=100000)
    peer_id = models.CharField(max_length=100000)

