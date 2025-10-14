from django.shortcuts import render

def home(request):
    return render(request, 'web_app/home.html')

def menu(request):
    return render(request, 'web_app/menu.html')

def order(request):
    return render(request, 'web_app/order.html')

def reservation(request):
    return render(request, 'web_app/reservation.html')

def about_contact(request):
    return render(request, 'web_app/about_contact.html')