from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .models import Profile
import uuid 

def login_user(request):
    # logout(request)
    if request.user.is_authenticated:
        return redirect('/my-tasks')
    if request.method == 'POST':
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        try:
            user_obj = User.objects.filter(email = email).first()
            if user_obj is None:
                messages.error(request, "Email not found. Please enter the correct email or register!!")
                return redirect('')
            
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if not profile_obj.is_verified:
                messages.error(request, "Please verify your email first")
                return redirect('')
            
            user = authenticate(username = user_obj.username, password = password)            
            if user is None:
                messages.error(request, "Wrong Password. Please try again!")
                return redirect("")
            else:
                login(request, user)
                return redirect('/my-tasks')
            
        except Exception as e:
            print(e)
    return render(request, 'users/login.html', {'title': 'Login'})


def register(request):
    if request.user.is_authenticated:
        return redirect('/my-tasks')
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        try:
            if User.objects.filter(email = email).first():
                messages.success(request, "You are already a user!!")
                return redirect('/auth/login')
        
            user_obj = User.objects.create_user(username=username, email=email, password=password)
            # user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj, auth_token=auth_token)
            profile_obj.save()
            
            send_verification_mail(auth_token, email, username)
            messages.success(request, "Please check your email for verfication!!")
            
        except Exception as e:
          print('An exception occurred', e)
        

    return render(request, 'users/register.html', {'title': 'Register'})


def send_verification_mail(token, email, username):
    subject = "Email Verification To-Do list"
    message = f'''
    
    Hi {username}, 
    
    Please click the below link to verify your account
    http://localhost:8000/auth/verify-user/{token}
    
    Thank You for considering To-Do List
    
    '''
                
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list) 

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "Your email is already verified. Login")
                return redirect('/auth/login')
            else:
                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request, "Congratulations your email has been verified. Please Log in")
                return redirect('/auth/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        
def errors(request):
    return HttpResponse("<h3>Error</h3>")

def signout(request):
    logout(request)
    return redirect('/auth/login')