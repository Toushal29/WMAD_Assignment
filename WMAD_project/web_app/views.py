from django.shortcuts import render

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
