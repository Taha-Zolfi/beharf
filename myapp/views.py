from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.utils import timezone
from .models import customuser , friendship
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        if 'signup' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            age = request.POST['age']
            city = request.POST['city']

            if len(username) < 4:
                messages.info(request, 'نام کاربری باید حداقل دارای 4 حروف انگلیسی باشد')
            # Validate password length and characters
            elif len(password) < 8 and not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
                messages.info(request, 'رمز عبور باید حداقل دارای 8 حروف انگلیسی و اعداد باشد')
            elif customuser.objects.filter(username=username).exists():
                messages.info(request, 'این نام کاربری قبلا استفاده شده')
            else:
                noga = customuser.objects.create_user(username=username, password=password, name=name, age=age, city=city)
                noga.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')

        else:
            username = request.POST['username']
            password = request.POST['password']

            # Validate username length and characters
            if len(username) < 4:
                messages.info(request, 'نام کاربری باید حداقل دارای 4 حروف انگلیسی باشد')
            # Validate password length and characters
            elif len(password) < 8 and not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
                messages.info(request, 'رمز عبور باید حداقل دارای 8 حروف انگلیسی و اعداد باشد')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    messages.info(request, 'نام کاربری یا رمز عبورت مشکل داره یا وجود نداره')
    
    return render(request, 'login.html')

def send_friend_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            receiver = customuser.objects.get(username=username)
            if receiver == request.user:
                messages.error(request, "You cannot send a friend request to yourself!")
            elif friendship.objects.filter(sender=request.user, receiver=receiver).exists():
                messages.error(request, "A friend request between you and this user already exists or you are already friends.")
            else:
                friendship.objects.create(sender=request.user, receiver=receiver)
                messages.success(request, "Friend request sent.")
        except customuser.DoesNotExist:
            messages.error(request, "User not found.")

    return redirect('friend_list')

def friend_list(request):
    friend_requests = friendship.objects.filter(receiver=request.user, status='pending')
    friends = friendship.objects.filter(sender=request.user, status='accepted') | friendship.objects.filter(receiver=request.user, status='accepted')
    
    context = {
        'friend_requests': friend_requests,
        'friends': friends,
    }
    return render(request, 'friend_list.html', context)

def accept_request(request, request_id):
    Friendship = get_object_or_404(friendship, id=request_id, receiver=request.user)
    Friendship.status = 'accepted'
    Friendship.save()
    return redirect('friend_list')

def reject_request(request, request_id):
    Friendship = get_object_or_404(friendship, id=request_id, receiver=request.user)
    Friendship.status = 'rejected'
    Friendship.save()
    return redirect('friend_list')    


@login_required(login_url='login/')
def home(request):

    return render(request, 'home.html')


@login_required(login_url='login/')
def profile(request):
    user = request.user
    # Initialize variables
    name = None
    age = None
    city = None

    if request.method == 'POST':
        # Check if 'name', 'age', and 'city' are present in the POST data
        if 'name' in request.POST:
            name = request.POST['name']
            user.name = name
            user.save()

        if 'age' in request.POST:
            age = request.POST['age']
            user.age = age
            user.save()

        if 'city' in request.POST:
            city = request.POST['city']
            user.city = city
            user.save()

        messages.info(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})


@login_required(login_url='login/')
def video(request):
    return render(request, 'video.html')

@login_required(login_url='login/')
def text(request):
    return render(request, 'text.html')
@login_required(login_url='login/')
def ttest(request):
    return render(request, 'ttest.html')
