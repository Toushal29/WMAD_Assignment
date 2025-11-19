from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from web_app.models import Users

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        admin_user_id = request.session.get("admin_user_id")

        if not admin_user_id:
            return redirect("admin_login")

        user = Users.objects.filter(id=admin_user_id).first()

        if not user or not (user.role == "admin" or user.is_superuser):
            return redirect("admin_login")

        request.admin_user = user   # attach logged admin user

        return view_func(request, *args, **kwargs)

    return wrapper


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and (user.role == "admin" or user.is_superuser):

            # STORE ADMIN LOGIN SEPARATELY
            request.session["admin_user_id"] = user.id

            return redirect("admin_dashboard")

        messages.error(request, "Invalid admin credentials")

    return render(request, "admin_site/login.html")


def admin_logout(request):
    # Clear only the admin session, NOT the customer session
    if "admin_user_id" in request.session:
        del request.session["admin_user_id"]

    return redirect('admin_login')


@admin_required
def admin_dashboard(request):
    return render(
        request, 
        'admin_site/dashboard.html', 
        {
            'active_tab': 'dashboard',
            'admin_user': request.admin_user,
        }
    )

@admin_required
def reservation_page(request):
    return render(
        request, 
        'admin_site/reservation.html', 
        {
            'active_tab': 'reservation',
            'admin_user': request.admin_user,
        }
    )

@admin_required
def edit_menu_page(request):
    return render(
        request, 
        'admin_site/edit_menu.html', 
        {
            'active_tab': 'edit_menu',
            'admin_user': request.admin_user,
        }
    )

@admin_required
def feedback_page(request):
    return render(
        request, 
        'admin_site/feedback.html', 
        {
            'active_tab': 'feedback',
            'admin_user': request.admin_user,
        }
    )

@admin_required
def customer_details_page(request):
    return render(
        request, 
        'admin_site/customer_details.html', 
        {
            'active_tab': 'customer_details',
            'admin_user': request.admin_user,
        }
    )

@admin_required
def edit_price_page(request):
    return render(
        request, 
        'admin_site/edit_price.html', 
        {
            'active_tab': 'edit_price',
            'admin_user': request.admin_user,
        }
    )

@admin_required
def orders_page(request):
    return render(
        request, 
        'admin_site/orders.html', 
        {
            'active_tab': 'orders',
            'admin_user': request.admin_user,
        }
    )
