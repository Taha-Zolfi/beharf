from myapp.views import home, video, text, login, logout
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('video/', video, name='video'),
    path('text/', text, name='text'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]