from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from .models import Special, MenuItem


# ===========================
# MAIN PAGES
# ===========================

def home(request):
    special = Special.objects.filter(is_active=True).first()
    return render(request, 'web_app/main_page/home.html', {'special': special})


def menu(request):
    items = MenuItem.objects.filter(available=True)
    
    return render(request, 'web_app/main_page/menu.html', {'items': items})


def order(request):
    return render(request, 'web_app/main_page/order.html')


def reservation(request):
    return render(request, 'web_app/main_page/reservation.html')


def about_contact(request):
    return render(request, 'web_app/main_page/about_contact.html')


# ===========================
# AUTH
# ===========================

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'web_app/entry/login.html')


def user_logout(request):
    auth_logout(request)
    return redirect('login')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        auth_login(request, user)
        messages.success(request, f"Welcome, {username}!")
        return redirect('home')

    return render(request, 'web_app/entry/signup.html')


# ===========================
# OTHER PAGES
# ===========================

def privacy_policy(request):
    return render(request, 'web_app/other_pages/privacy_policy.html')

