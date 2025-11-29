# C:\Users\toush\Desktop\WMAD_Assignment\WMAD_project\web_app\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import (Cart, CartItem, Order, OrderItem, Menu, Special, Customer)


User = get_user_model()


def home(request):
    special = Special.objects.filter(is_active=True).first()
    return render(request, 'web_app/main_page/home.html', {'special': special})


def menu(request):
    items = Menu.objects.all()
    return render(request, 'web_app/main_page/menu.html', {'items': items})


def order(request):
    items = Menu.objects.all()[:8]
    total_menu_count = Menu.objects.count()
    return render(request, 'web_app/main_page/order.html', {
        "items": items,
        "total_items": total_menu_count,
    })


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

@login_required
def profile_page(request):
    user = request.user

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')


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
        login(request, user)
        messages.success(request, f"Welcome, {username}!")
        return redirect('home')

    return render(request, 'registration/signup.html')

def load_more_menu(request):
    offset = int(request.GET.get("offset", 0))
    limit = 8
    items = list(Menu.objects.all()[offset:offset + limit].values())
    return JsonResponse({"items": items})


@login_required
@require_POST
def add_to_cart(request):
    menu_id = request.POST.get("menu_id")

    if not menu_id or not menu_id.isdigit():
        return JsonResponse({"error": "Invalid menu id"}, status=400)

    qty = int(request.POST.get("quantity", 1))
    if qty < 1:
        return JsonResponse({"error": "Invalid quantity"}, status=400)

    menu_item = get_object_or_404(Menu, pk=menu_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu=menu_item,
        defaults={"quantity": qty, "unit_price": menu_item.price}
    )

    if not created:
        cart_item.quantity += qty
        cart_item.save()

    return JsonResponse({"message": "Added to cart!"})


@login_required
def get_cart_items(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    items = [{
        "menuID": ci.menu.menuID,
        "name": ci.menu.menuName,
        "qty": ci.quantity,
        "subtotal": float(ci.subtotal),
    } for ci in cart.cartitem_set.all()]

    return JsonResponse({"items": items})


@login_required
@require_POST
def remove_from_cart(request):
    menu_id = request.POST.get("menu_id")

    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({"error": "Cart not found"}, status=404)

    cart_item = cart.cartitem_set.filter(menu__menuID=menu_id).first()
    if not cart_item:
        return JsonResponse({"error": "Item not found"}, status=404)

    cart_item.delete()
    return JsonResponse({"message": "Item removed"})


@login_required
@require_POST
def clear_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.cartitem_set.all().delete()
    return JsonResponse({"message": "Cart cleared"})


@login_required
@require_POST
def confirm_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()

    if not items.exists():
        return JsonResponse({"error": "Cart is empty"}, status=400)

    delivery_mode = request.POST.get("delivery_mode", "").strip()

    if delivery_mode in ["pickup", "dinein"]:
        delivery_address = "NONE"
    elif delivery_mode == "":
        return JsonResponse({"error": "Please choose an order option"}, status=400)
    else:
        delivery_address = request.POST.get("delivery_address", "").strip()

    order = Order.objects.create(
        customer=request.user,
        totalamount=cart.total_amount(),
        order_type=delivery_mode,
        deliveryaddress=delivery_address,
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            menu=item.menu,
            quantity=item.quantity,
            unit_price=item.unit_price
        )

    items.delete()
    return JsonResponse({"message": "Order confirmed"})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-order_date', '-order_time')
    return render(request, "web_app/main_page/my_orders.html", {"orders": orders})


@login_required
@require_POST
def cancel_order(request, orderid):
    order = get_object_or_404(Order, orderID=orderid, customer=request.user)

    if order.status == "completed":
        return JsonResponse({"error": "Completed orders cannot be cancelled."}, status=400)

    order.status = "cancelled"
    order.save()
    return redirect("my_orders")
