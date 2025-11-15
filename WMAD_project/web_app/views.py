
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages


def home(request):
    return render(request, 'web_app/main_page/home.html')

def menu(request):
    return render(request, 'web_app/main_page/menu.html')

def order(request):
    return render(request, 'web_app/main_page/order.html')

def reservation(request):
    return render(request, 'web_app/main_page/reservation.html')

def about_contact(request):
    return render(request, 'web_app/main_page/about_contact.html')

def login(request):
    return render(request, 'web_app/entry/login.html')

def signup(request):
    return render(request, 'web_app/entry/signup.html')

def privacy_policy(request):
    return render(request, 'web_app/other_pages/privacy_policy.html')

from django.shortcuts import render
from web_app.models import Special  # adjust the import path as per your app name

def home(request):
    special = Special.objects.filter(is_active=True).first()
    return render(request, 'web_app/main_page/home.html', {'special': special})

from django.shortcuts import render, redirect

from django.contrib import messages

# web_app/views.py



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def home(request):
    return render(request, 'web_app/main_page/home.html')  # your home page


def user_logout(request):
    auth_logout(request)
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    # ✅ Correct template path
    return render(request, 'web_app/entry/login.html')

# web_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Auto-login after signup
        auth_login(request, user)
        messages.success(request, f"Welcome, {username}! Your account has been created.")
        return redirect('home')

    return render(request, 'web_app/entry/signup.html')
