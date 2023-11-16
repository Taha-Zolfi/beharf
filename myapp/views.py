from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.utils import timezone
from .models import customuser
from django.http import JsonResponse
from django.http import HttpResponse


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
            
            if customuser.objects.filter(username=username).exists():
                messages.info(request, 'این یوزرنیم قبلا استفاده شده')
            else :
                noga = customuser.objects.create_user(username=username, password=password, name=name , age=age ,city=city)
                noga.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')

        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')



@login_required(login_url='login/')
def home(request):

    return render(request, 'home.html')

@login_required(login_url='login/')
def video(request):

    return render(request, 'video.html')

@login_required(login_url='login/')
def text(request):
    
    return render(request, 'text.html')
