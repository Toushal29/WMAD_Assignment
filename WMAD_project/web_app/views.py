from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Customer, Special, Menu

#MAIN PAGES
def home(request):
    special = Special.objects.filter(is_active=True).first()
    return render(request, 'web_app/main_page/home.html', {'special': special})

def menu(request):
    items = Menu.objects.all()
    return render(request, 'web_app/main_page/menu.html', {'items': items})

def order(request):
    return render(request, 'web_app/main_page/order.html')

def reservation(request):
    return render(request, 'web_app/main_page/reservation.html')

def about_contact(request):
    return render(request, 'web_app/main_page/about_contact.html')

def privacy_policy(request):
    return render(request, 'web_app/other_pages/privacy_policy.html')

#USER SIGNUP
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

#ACCOUNT PAGES
def profile_page(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, user=user, instance=user)
        if form.is_valid():
            form.save()
            address = form.cleaned_data.get('address')
            customer, created = Customer.objects.get_or_create(user=user)
            customer.address = address
            customer.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(user=user, instance=user)

    return render(request, 'web_app/account/profile.html', {
        'section': 'profile',
        'form': form
    })

def settings_page(request):
    return render(request, 'web_app/account/settings.html', {'section': 'settings'})

def orders_page(request):
    return render(request, 'web_app/account/orders.html', {'section': 'orders'})

def reviews_page(request):
    return render(request, 'web_app/account/reviews.html', {'section': 'reviews'})

@login_required
def delete_account(request):
    user = request.user

    if request.method == 'POST':
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted.")
        return redirect('home')

    return render(request, 'web_app/account/confirm_delete.html')

#AUTHENTICATION
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

#SIMPLE AUTH (entry folder)
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'web_app/entry/login.html')

def user_logout(request):
    logout(request)
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

        login(request, user)
        messages.success(request, f"Welcome, {username}!")
        return redirect('home')

    return render(request, 'web_app/entry/signup.html')