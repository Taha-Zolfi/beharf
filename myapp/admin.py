from django.contrib import admin
from .models import customuser,waiting_users
# Register your models here.

admin.site.register(customuser)
admin.site.register(waiting_users)