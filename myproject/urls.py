# project_directory/urls.py
from myapp import views
from myapp.views import home, video, text, login, profile , ttest
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('video/', video, name='video'),
    path('text/', text, name='text'),
    path('ttest/', ttest, name='ttest'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('friend-list/', views.friend_list, name='friend_list'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('friend-list/', views.friend_list, name='friend_list'),
    path('send-friend-request/', views.send_friend_request, name='send_friend_request'),
]