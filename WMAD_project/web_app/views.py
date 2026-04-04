# C:\Users\...\WMAD_Assignment\WMAD_project\web_app\views.py

# this file defines the view functions for the web application, handling the logic for rendering templates, processing forms, managing user authentication and API

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, ProfileUpdateForm, ReviewForm
from .models import Cart, Customer, Menu, Order, OrderItem, Reservation, Review, Special

# API REST FRAMEWORKS
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


# API Views
# Delete the user's token to log them out
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    try:
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=200)
    except Exception:
        return Response({"error": "No active token found."}, status=400)

# register and auto-login
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    serializer = serializers.CustomerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()        # This returns the Customer instance
        token, _ = Token.objects.get_or_create(user=customer.user)

        # Combine the data
        response_data = serializer.data
        response_data['token'] = token.key

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny]) # This allows guests to access this specific view
def api_menus(request):
    menus = Menu.objects.all()
    serializer = serializers.MenuSerializer(menus, many=True)
    return Response(serializer.data)

# update profile
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_upd_profile(request, pk):
    customer = get_object_or_404(Customer.objects.select_related('user'), id=pk)
    if request.user.id != customer.user.id:
        return Response({"detail": "You do not have permission to edit this profile."},status=status.HTTP_403_FORBIDDEN)
    serializer = serializers.CustomerUpdateSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete profile
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_profile(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    if request.user.id != customer.user.id:     # check if user own profile
        return Response({"detail": "You do not have permission to delete this profile."}, status=status.HTTP_403_FORBIDDEN)
    # delete
    user = customer.user
    user.delete()
    return Response({"message": "User and Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_menu_detail(request,pk):
    menu = get_object_or_404(Menu, id=pk)
    serializer = serializers.MenuSerializer(menu)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_customers(request):
    # select_related('user') joins the tables at the DB level
    customers = Customer.objects.select_related('user').all()
    serializer = serializers.CustomerSerializer(customers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_profile(request,pk):
    customer = get_object_or_404(Customer.objects.select_related('user'), id=pk)
    serializer = serializers.CustomerSerializer(customer)
    return Response(serializer.data)

# Reviews
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_reviews(request):
    # Use the related_name "reviews" from your User model
    reviews = request.user.reviews.all()
    serializer = serializers.ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_upd_reviews(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return Response({"detail": "You cannot edit someone else's review."}, status=status.HTTP_403_FORBIDDEN)
    serializer = serializers.ReviewUpdateSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_reviews(request,review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return Response({"detail": "You cannot delete someone else's review."}, status=status.HTTP_403_FORBIDDEN)
    review.delete()
    return Response({"message": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# Orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_order_list(request):
    orders = request.user.orders.all()
    serializer = serializers.OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return Response({"detail": "You do not have permission to view this order."}, status=status.HTTP_403_FORBIDDEN)
    items = order.items.select_related('menu').all()
    serializer = serializers.OrderItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != Order.STATUS_PENDING:
        return Response({"detail": f"Order cannot be cancelled because it is currently {order.status}."},status=status.HTTP_400_BAD_REQUEST)
    order.status = 'cancelled' # Or Order.STATUS_CANCELLED if you defined that constant
    order.save()

    return Response({"message": f"Order #{order_id} has been successfully cancelled."},status=status.HTTP_200_OK)


# reservations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_reservation_list(request):
    reservations = Reservation.objects.select_related('customer__user').filter(
        customer__user=request.user
    )
    serializer = serializers.ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_del_reservation(request, resev_id):
    reservation = get_object_or_404(Reservation, id=resev_id)
    if reservation.customer.user != request.user:
        return Response({"detail": "You cannot cancel someone else's reservation."}, status=status.HTTP_403_FORBIDDEN)
    if reservation.status != Reservation.STATUS_PENDING:
        return Response({"detail": f"Reservation cannot be cancelled because it is already {reservation.status}."}, status=status.HTTP_400_BAD_REQUEST)
    reservation.status = Reservation.STATUS_CANCELLED
    reservation.save()
    return Response({"message": "Reservation cancelled successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_reservation(request):
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        return Response(
{"detail": "Customer profile not found. Please complete your profile first."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = serializers.ReservationCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Ordering
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_checkout_preview(request):
    """
    Step 1: The 'Get Quote' step. 
    Mobile app sends the local list, server returns the official total.
    """
    serializer = serializers.CheckoutSessionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    items_data = serializer.validated_data['items']
    subtotal = 0
    validation_errors = []
    confirmed_items = []

    for item in items_data:
        menu_item = Menu.objects.filter(id=item['menu_id']).first()
        
        if not menu_item:
            validation_errors.append(f"Item ID {item['menu_id']} not found.")
            continue
        
        if not menu_item.available:
            validation_errors.append(f"{menu_item.name} is currently out of stock.")
            continue

        item_subtotal = menu_item.price * item['quantity']
        subtotal += item_subtotal
        
        confirmed_items.append({
            "name": menu_item.name,
            "price": str(menu_item.price),
            "quantity": item['quantity'],
            "subtotal": str(item_subtotal)
        })

    if validation_errors:
        return Response({"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST)

    # Business Logic: Add delivery fee or tax
    delivery_fee = 5.00
    grand_total = float(subtotal) + delivery_fee

    return Response({
        "summary": {
            "items": confirmed_items,
            "subtotal": str(subtotal),
            "delivery_fee": str(delivery_fee),
            "grand_total": str(grand_total)
        },
        "can_proceed": True
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_place_order(request):
    """
    Step 2: The 'Commit' step.
    Actually saves the Order and OrderItems to the database.
    """
    serializer = serializers.CheckoutSessionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    items_data = serializer.validated_data['items']
    
    # 1. Start a transaction (optional but recommended)
    from django.db import transaction
    try:
        with transaction.atomic():
            # 2. Create the Order object
            # We calculate price again on server to prevent price-hacking from the app
            order = Order.objects.create(
                user=request.user,
                total_price=0, # Will update this in a second
                status=Order.STATUS_PENDING
            )

            final_total = 0
            for item in items_data:
                menu_item = get_object_or_404(Menu, id=item['menu_id'], available=True)
                
                OrderItem.objects.create(
                    order=order,
                    menu=menu_item,
                    quantity=item['quantity'],
                    price=menu_item.price
                )
                final_total += menu_item.price * item['quantity']

            # 3. Update the final price (including $5 delivery)
            order.total_price = final_total + 5
            order.save()

            return Response({
                "message": "Order placed successfully!",
                "order_id": order.id,
                "total": str(order.total_price)
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

















# function to get customer profile or redirect if not found, used in multiple views to avoid code duplication
def get_customer_or_redirect(request, redirect_name="home"):
    customer = Customer.objects.filter(user=request.user).first()
    if customer:
        return customer, None

    messages.error(request, "Customer profile not found for this account.")
    return None, redirect(redirect_name)

# function to calculate cart total for a user, used in checkout and order confirmation views
def cart_total_for_user(user):
    return sum(item.line_total for item in Cart.objects.filter(user=user).select_related("menu"))

# views for main pages
def home(request):
    special = Special.objects.filter(is_active=True).first()
    return render(request, "web_app/main_page/home.html", {"special": special})

# menu view now also includes recent reviews to show on the menu page, and uses select_related to optimize queries
def menu(request):
    items = Menu.objects.filter(available=True)
    reviews = Review.objects.select_related("user", "menu").order_by("-created_at")[:10]
    return render(
        request,
        "web_app/main_page/menu.html",
        {
            "items": items,
            "reviews": reviews,
        },
    )

# order view now checks if user is authenticated to show cart status, and also counts total menu items for display
def order(request):
    items = Menu.objects.filter(available=True)
    total_menu_count = items.count()

    if request.user.is_authenticated:
        cart_has_items = Cart.objects.filter(user=request.user).exists()
    else:
        cart_has_items = False

    return render(
        request,
        "web_app/main_page/order.html",
        {
            "items": items,
            "total_items": total_menu_count,
            "cart_has_items": cart_has_items,
        },
    )


@login_required
# Checkout from cart
def checkout(request):
    items = Cart.objects.filter(user=request.user).select_related("menu")
    total = cart_total_for_user(request.user)
    return render(
        request,
        "web_app/main_page/checkout.html",
        {
            "items": items,
            "total": total,
        },
    )

# about/contact and privacy policy views are simple static pages, no changes needed
def about_contact(request):
    return render(request, "web_app/main_page/about_contact.html")

def privacy_policy(request):
    return render(request, "web_app/other_pages/privacy_policy.html")


# signup new user
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# user login + redirect
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                request.session.set_expiry(604800)

                if user.is_staff or user.is_superuser:
                    return redirect("/admin/")

                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


# logout view simply logs out
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_page(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, user=user, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(user=user, instance=user)
    return render(
        request,
        "web_app/account/profile.html",
        {"section": "profile", "form": form},
    )


@login_required
# settings page
def settings_page(request):
    return render(request, "web_app/account/settings.html", {"section": "settings"})


@login_required
# delete account
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("home")
    return render(request, "web_app/account/confirm_delete.html")


# reservation view
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
            status=Reservation.STATUS_PENDING,
        )
        messages.success(request, "Reservation submitted.")
        return redirect("reservation")

    customer = None
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()

    return render(
        request,
        "web_app/main_page/reservation.html",
        {"customer_profile": customer},
    )


# AJAX view to load more menu items for infinite scrolling on the menu page
def load_more_menu(request):
    offset = int(request.GET.get("offset", 0))
    limit = 8
    items = list(
        Menu.objects.filter(available=True)[offset : offset + limit].values(
            "id",
            "name",
            "description",
            "detail_description",
            "price",
            "image",
            "category",
            "available",
        )
    )
    return JsonResponse({"items": items})


@login_required
# AJAX view to add a menu item to the cart
@require_POST
def add_to_cart(request):
    menu_id = request.POST["menu_id"]
    qty = int(request.POST.get("quantity", 1))

    item = get_object_or_404(Menu, pk=menu_id, available=True)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        menu=item,
        defaults={"quantity": qty},
    )
    if not created:
        cart_item.quantity += qty
        cart_item.save()

    return JsonResponse({"message": "Added"})


@login_required
# AJAX view to get current cart items for the logged-in user
def get_cart_items(request):
    items = [
        {
            "menu_id": ci.menu_id,
            "name": ci.menu.name,
            "qty": ci.quantity,
            "subtotal": float(ci.line_total),
        }
        for ci in Cart.objects.filter(user=request.user).select_related("menu")
    ]
    return JsonResponse({"items": items})

# AJAX view to remove a menu item from the cart
@login_required
@require_POST
def remove_from_cart(request):
    item = Cart.objects.filter(
        user=request.user,
        menu_id=request.POST["menu_id"],
    ).first()
    if item:
        item.delete()
    return JsonResponse({"message": "removed"})

# AJAX view to clear all items from the cart for the logged-in user
@login_required
@require_POST
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return JsonResponse({"message": "cleared"})

# AJAX view to confirm an order
@login_required
@require_POST
def confirm_order(request):
    items = Cart.objects.filter(user=request.user).select_related("menu")
    if not items.exists():
        return JsonResponse({"error": "empty"}, status=400)

    customer = Customer.objects.filter(user=request.user).first()
    if not customer:
        return JsonResponse({"error": "customer_missing"}, status=400)

    order = Order.objects.create(
        user=request.user,
        total_price=cart_total_for_user(request.user),
        status=Order.STATUS_PENDING,
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            menu=item.menu,
            quantity=item.quantity,
            price=item.menu.price,
        )

    items.delete()

    return JsonResponse({"success": True, "redirect": "/profile/my_orders/"})


# reservation view
@login_required
def my_orders(request):
    customer, missing_response = get_customer_or_redirect(request, "home")
    if missing_response:
        return missing_response

    orders = Order.objects.filter(user=customer.user).prefetch_related("items__menu")
    return render(request, "web_app/main_page/my_orders.html", {"orders": orders})


# cancel order view
@login_required
@require_POST
def cancel_order_action(request, order_id):
    # Retrieve customer profile
    customer, missing_response = get_customer_or_redirect(request, "orders")
    if missing_response:
        return missing_response

    # Ensure the order belongs to the user
    order = get_object_or_404(Order, pk=order_id, user=customer.user)
    
    # Only allow cancellation if the order is still pending
    if order.status == Order.STATUS_PENDING:
        order.status = 'cancelled' # Matches the logic in your HTML status classes
        order.save()
        messages.success(request, f"Order #{order_id} has been cancelled.")
    else:
        messages.error(request, "This order is already being prepared or completed and cannot be cancelled.")
        
    return redirect("orders")

# account views for orders, reservations, and reviews
@login_required
def account_orders(request):
    customer, missing_response = get_customer_or_redirect(request, "home")
    if missing_response:
        return missing_response

    orders = Order.objects.filter(user=customer.user).prefetch_related("items__menu")
    return render(
        request,
        "web_app/account/orders.html",
        {"section": "orders", "orders": orders},
    )

@login_required
def account_reservations(request):
    customer, missing_response = get_customer_or_redirect(request, "home")
    if missing_response:
        return missing_response

    reservations = Reservation.objects.filter(customer=customer)
    return render(
        request,
        "web_app/account/reservations.html",
        {
            "section": "reservations",
            "reservations": reservations,
        },
    )

@login_required
@require_POST
def cancel_reservation(request, reservation_id):
    customer, missing_response = get_customer_or_redirect(request, "reservations")
    if missing_response:
        return missing_response

    reservation = get_object_or_404(Reservation, pk=reservation_id, customer=customer)

    if reservation.status == Reservation.STATUS_PENDING:
        reservation.status = Reservation.STATUS_CANCELLED
        reservation.save()
        messages.success(request, "Reservation cancelled successfully.")
    else:
        messages.error(request, "Only pending reservations can be cancelled.")
    return redirect("reservations")

@login_required
def account_reviews(request):
    customer, missing_response = get_customer_or_redirect(request, "home")
    if missing_response:
        return missing_response

    reviews = Review.objects.filter(user=customer.user).select_related("menu")
    return render(
        request,
        "web_app/account/reviews.html",
        {
            "section": "reviews",
            "reviews": reviews,
        },
    )



# AJAX view to add a menu item review
@login_required
def add_review(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    customer, missing_response = get_customer_or_redirect(request, "menu")
    if missing_response:
        return missing_response

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                user=customer.user,
                menu=menu_item,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "comment": form.cleaned_data.get("comment", ""),
                },
            )
            messages.success(request, "Review submitted!")
            return redirect("menu")

    return redirect("menu")

# AJAX view to add a restaurant review
@login_required
def add_restaurant_review(request):
    customer, missing_response = get_customer_or_redirect(request, "reviews")
    if missing_response:
        return missing_response

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                user=customer.user,
                menu=None,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "comment": form.cleaned_data.get("comment", ""),
                },
            )
            messages.success(request, "Restaurant review submitted!")
    return redirect("reviews")

# view to display all reviews
def view_reviews(request):
    menu_reviews = Review.objects.filter(menu__isnull=False).select_related("menu", "user")
    restaurant_reviews = Review.objects.filter(menu__isnull=True).select_related("user")
    return render(
        request,
        "web_app/main_page/reviews.html",
        {
            "menu_reviews": menu_reviews,
            "restaurant_reviews": restaurant_reviews,
        },
    )

# view to edit a review
@login_required
def edit_review(request, review_id):
    customer, missing_response = get_customer_or_redirect(request, "reviews")
    if missing_response:
        return missing_response

    review = get_object_or_404(Review, pk=review_id, user=customer.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated!")
            return redirect("reviews")
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "web_app/account/edit_review.html",
        {"form": form, "review": review},
    )

# view to delete a review, checks if the review belongs to the logged-in user, and deletes it with a confirmation message, then redirects back to the reviews page
@login_required
def delete_review(request, review_id):
    customer, missing_response = get_customer_or_redirect(request, "reviews")
    if missing_response:
        return missing_response

    review = get_object_or_404(Review, pk=review_id, user=customer.user)
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect("reviews")