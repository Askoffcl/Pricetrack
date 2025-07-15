from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import userRegister,shopRegister
import random
from django.core.mail import send_mail
from django.conf import settings
def home(request):
    return render(request, 'home.html')

def userRegistraion(request):
    if request.method == "POST":
        form = userRegister(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            if Register.objects.filter(username = username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'userregister.html')
            email = form.cleaned_data['email']
            if Register.objects.filter(email = email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'userregister.html')
            password = form.cleaned_data['password']
            password = make_password(password)
            user = form.save(commit = False)
            user.role = "User"
            user.password = password
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request,'invalid form data')
    form = userRegister()
    return render(request, 'userRegistration.html',{'form':form})

def shopRegistraion(request):
    if request.method == "POST":
        form = shopRegister(request.POST,request.FILES)
        if form.is_valid():
            ownername = form.cleaned_data['name']
            if Register.objects.filter(name = ownername).exists():
                messages.error(request, 'ownername already exists')
                return render(request, 'shopregister.html')
            email = form.cleaned_data['email']
            if Register.objects.filter(email = email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'shopregister.html')
            password = form.cleaned_data['password']
            password = make_password(password)
            user = form.save(commit=False)
            user.role = "retailer"
            user.password = password
            user.username = ownername.lower()
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request,'invalid form data')
    form = shopRegister()
    return render(request, 'shopRegistration.html',{'form':form})

def loginall(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request,"login success")
                return redirect('/homepage')
            else:
                messages.error(request, 'User is deactivated')
                return render(request, 'login.html')
        else:
            messages.error(request, 'invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutall(request):
    logout(request)
    return redirect('/')

@login_required
def homepage(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request,'about.html')




def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if Register.objects.filter(email = email).exists():
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            send_mail(
                 subject = "one time password",
                 message = f"Your one time otp is {otp}",
                 from_email = settings.EMAIL_HOST_USER,
                 recipient_list = [email],
                 fail_silently = True
                 
             )
            user = Register.objects.get(email = email)
            user.password  = make_password(otp)
            user.save()
            return redirect('login')
      
    
    return render(request,'forgotPassword.html')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('confirm')
        user = request.user
        user.password  = make_password(password)
        user.save()
        return redirect('login')
    return render(request,'resetPassword.html')