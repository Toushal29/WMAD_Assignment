from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import (
    Cart, CartItem, Order, OrderItem,
    Menu, Special, Customer, Reservation
)
from datetime import datetime

# HOME
def home(request):
    special = Special.objects.filter(is_active=True).first()
    return render(request, "web_app/main_page/home.html", {"special": special})

# MENU
def menu(request):
    items = Menu.objects.all()
    return render(request, "web_app/main_page/menu.html", {"items": items})

# ORDER PAGE (FIXED WITH CART CHECK)
def order(request):
    items = Menu.objects.all()
    total_menu_count = Menu.objects.count()

    # NEW: Check if cart has items
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_has_items = cart and cart.cartitem_set.exists()
    else:
        cart_has_items = False

    return render(request, "web_app/main_page/order.html", {
        "items": items,
        "total_items": total_menu_count,
        "cart_has_items": cart_has_items,  # ADDED
    })

# CHECKOUT PAGE
@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    total = cart.total_amount()

    return render(request, "web_app/main_page/checkout.html", {
        "items": items,
        "total": total
    })

# ABOUT & CONTACT
def about_contact(request):
    return render(request, "web_app/main_page/about_contact.html")

# PRIVACY PAGE
def privacy_policy(request):
    return render(request, "web_app/other_pages/privacy_policy.html")

# SIGNUP
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# LOGIN
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                request.session.set_expiry(604800)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("home")

# PROFILE
@login_required
def profile_page(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, user=user, instance=user)
        if form.is_valid():
            form.save()
            customer, _ = Customer.objects.get_or_create(user=user)
            customer.address = form.cleaned_data.get("address")
            customer.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(user=user, instance=user)
    return render(request, "web_app/account/profile.html", {"section": "profile", "form": form})

# SETTINGS
def settings_page(request):
    return render(request, "web_app/account/settings.html", {"section": "settings"})

# DELETE ACCOUNT
@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("home")
    return render(request, "web_app/account/confirm_delete.html")

# RESERVATION PAGE
def reservation(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in.")
            return redirect("login")

        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            messages.error(request, "Customer data missing.")
            return redirect("reservation")

        Reservation.objects.create(
            customer=customer,
            reservation_date=request.POST.get("reservation_date"),
            reservation_time=request.POST.get("reservation_time"),
            party_size=request.POST.get("party_size"),
            seating_choice=request.POST.get("seating_choice"),
            allergy_info=request.POST.get("allergy_info"),
            status="pending"
        )
        messages.success(request, "Reservation submitted.")
        return redirect("reservation")

    return render(request, "web_app/main_page/reservation.html")

# LOAD MORE (AJAX)
def load_more_menu(request):
    offset = int(request.GET.get("offset", 0))
    limit = 8
    items = list(Menu.objects.all()[offset:offset+limit].values())
    return JsonResponse({"items": items})

# ADD TO CART
@login_required
@require_POST
def add_to_cart(request):
    menu_id = request.POST["menu_id"]
    qty = int(request.POST.get("quantity", 1))

    item = get_object_or_404(Menu, pk=menu_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, menu=item, defaults={"quantity": qty, "unit_price": item.price}
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

    return JsonResponse({"message": "Added"})

# GET CART
@login_required
def get_cart_items(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = [{
        "menuID": ci.menu.menuID,
        "name": ci.menu.menuName,
        "qty": ci.quantity,
        "subtotal": float(ci.subtotal)
    } for ci in cart.cartitem_set.all()]
    return JsonResponse({"items": items})

# REMOVE FROM CART
@login_required
@require_POST
def remove_from_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    item = cart.cartitem_set.filter(menu__menuID=request.POST["menu_id"]).first()
    if item:
        item.delete()
    return JsonResponse({"message": "removed"})

# CLEAR CART
@login_required
@require_POST
def clear_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.cartitem_set.all().delete()
    return JsonResponse({"message": "cleared"})

# CONFIRM ORDER
@login_required
@require_POST
def confirm_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()

    if not items.exists():
        return JsonResponse({"error": "empty"}, status=400)

    mode = request.POST.get("delivery_mode", "")
    address = request.POST.get("delivery_address", "")

    customer = Customer.objects.get(user=request.user)

    order = Order.objects.create(
        customer=customer,
        totalamount=cart.total_amount(),
        order_type=mode,
        deliveryaddress=address,
        status="pending",
    )

    for it in items:
        OrderItem.objects.create(
            order=order,
            menu=it.menu,
            quantity=it.quantity,
            unit_price=it.unit_price,
        )

    cart.cartitem_set.all().delete()

    return JsonResponse({"success": True, "redirect": "/profile/my_orders/"})

# MY ORDERS
@login_required
def my_orders(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer).order_by("-order_date")
    return render(request, "web_app/main_page/my_orders.html", {"orders": orders})

# CANCEL ORDER
@login_required
@require_POST
def cancel_order(request, orderid):
    customer = Customer.objects.get(user=request.user)
    order = get_object_or_404(Order, orderID=orderid, customer=customer)

    if order.status != "completed":
        order.status = "cancelled"
        order.save()

    return redirect("my_orders")

# ACCOUNT ORDERS
@login_required
def account_orders(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer).order_by("-order_date")
    return render(request, "web_app/account/orders.html", {"section": "orders", "orders": orders})

# ACCOUNT RESERVATIONS
@login_required
def account_reservations(request):
    customer = Customer.objects.get(user=request.user)
    reservations = Reservation.objects.filter(customer=customer).order_by("-reservation_date")
    return render(request, "web_app/account/reservations.html", {
        "section": "reservations",
        "reservations": reservations
    })
