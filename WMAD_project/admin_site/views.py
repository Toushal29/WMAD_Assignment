from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.db import models

from web_app.models import (
    Users,
    Customer,
    Reservation,
    Menu,
    Order,
    Reviews,
    OrderItem
)

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        # Admin must be logged in using Django's auth system
        if not request.user.is_authenticated:
            return redirect("admin_login")

        # Admin must have admin role or be superuser
        if not (request.user.role == "admin" or request.user.is_superuser):
            return redirect("admin_login")

        request.admin_user = request.user  # attach logged admin user

        return view_func(request, *args, **kwargs)

    return wrapper


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and (user.role == "admin" or user.is_superuser):
            # Use Django's built-in session
            login(request, user)

            # Keep admin logged in for 7 days
            request.session.set_expiry(86400 * 7)

            return redirect("admin_dashboard")
        
        messages.error(request, "Invalid admin credentials")
    return render(request, "admin_site/login.html")


def admin_logout(request):
    # Clear only the admin session, NOT the customer session
    logout(request)
    return redirect("admin_login")



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
    reservations = Reservation.objects.select_related('customer__user').all()

    return render(
        request,
        'admin_site/reservation.html',
        {
            'active_tab': 'reservation',
            'admin_user': request.admin_user,
            'reservations': reservations,
        }
    )

@admin_required
def edit_menu_page(request):
    menu_items = Menu.objects.all()

    return render(
        request,
        'admin_site/edit_menu.html',
        {
            'active_tab': 'edit_menu',
            'admin_user': request.admin_user,
            'menu_items': menu_items,
        }
    )

@admin_required
def feedback_page(request):
    reviews = Reviews.objects.select_related(
        'customer__user', 'menu'
    ).all()

    return render(
        request,
        'admin_site/feedback.html',
        {
            'active_tab': 'feedback',
            'admin_user': request.admin_user,
            'reviews': reviews,
        }
    )

@admin_required
def edit_price_page(request):
    menu_items = Menu.objects.all()

    return render(
        request,
        'admin_site/edit_price.html',
        {
            'active_tab': 'edit_price',
            'admin_user': request.admin_user,
            'menu_items': menu_items,
        }
    )

@admin_required
def orders_page(request):
    orders = (
        Order.objects
        .select_related('customer__user')
        .prefetch_related('orderitem_set__menu')
        .all()
    )

    return render(
        request,
        'admin_site/orders.html',
        {
            'active_tab': 'orders',
            'admin_user': request.admin_user,
            'orders': orders,
        }
    )

@admin_required
def customer_edit(request, id):
    """
    Loads a customer record so the admin can edit it.
    (Used for modal-based editing.)
    """
    customer = Customer.objects.select_related("user").filter(user_id=id).first()

    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("admin_customer_details")

    return render(
        request,
        "admin_site/customer_edit.html",   # only needed if you use a page version
        {
            "active_tab": "customer_details",
            "admin_user": request.admin_user,
            "customer": customer,
        }
    )


@admin_required
def customer_update(request, id):
    """
    Receives POST request from edit modal and updates the database.
    """
    customer = Customer.objects.select_related("user").filter(user_id=id).first()

    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("admin_customer_details")

    if request.method == "POST":
        user = customer.user

        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.phone_no = request.POST.get("phone_no", user.phone_no)
        user.save()

        customer.address = request.POST.get("address", customer.address)
        customer.save()

        messages.success(request, "Customer updated successfully.")
        return redirect("admin_customer_details")

    # fallback (should not really be hit)
    return redirect("admin_customer_details")

@admin_required
def customer_delete(request, id):
    customer = Customer.objects.filter(user_id=id).first()

    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("admin_customer_details")

    # Delete both Customer and User
    user = customer.user
    user.delete()

    messages.success(request, "Customer deleted successfully.")
    return redirect("admin_customer_details")


@admin_required
def customer_details_page(request):

    search = request.GET.get("search", "").strip()

    # If admin types something in search bar
    if search:
        customers = Customer.objects.select_related('user').filter(
            models.Q(user__first_name__icontains=search) |
            models.Q(user__last_name__icontains=search) |
            models.Q(user__email__icontains=search) |
            models.Q(user__username__icontains=search) |
            models.Q(user__phone_no__icontains=search) |
            models.Q(address__icontains=search)
        )
    else:
        customers = Customer.objects.select_related('user').all().order_by('-user_id')  # newest first

    return render(
        request,
        'admin_site/customer_details.html',
        {
            'active_tab': 'customer_details',
            'admin_user': request.admin_user,
            'customers': customers,
            'search': search,
        }
    )
