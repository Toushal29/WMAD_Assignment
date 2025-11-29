from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileUpdateForm
from .models import Customer
from django.contrib.auth.decorators import login_required
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

def privacy_policy(request):
    return render(request, 'web_app/other_pages/privacy_policy.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def profile_page(request):
    user = request.user
    # Redirect if not logged in
    if not user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, user=user, instance=user)
        if form.is_valid():
            form.save()
            # Update Customer address separately
            address = form.cleaned_data.get('address')
            customer, created = Customer.objects.get_or_create(user=user)
            customer.address = address
            customer.save()
            return redirect('profile')  # reload updated page
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


@login_required
def delete_account(request):
    user = request.user

    if request.method == 'POST':
        # Delete user and linked Customer record
        user.delete()

        logout(request)
        messages.success(request, "Your account has been deleted.")
        return redirect('home')

    return render(request, 'web_app/account/confirm_delete.html')