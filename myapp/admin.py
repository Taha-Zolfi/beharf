from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(customuser)
admin.site.register(waiting_users)
admin.site.register(UserCommunication)

admin.site.register(waiting_users_text)
admin.site.register(waiting_users_test)
admin.site.register(waiting_users_test_video)
admin.site.register(UserCommunication_text)

