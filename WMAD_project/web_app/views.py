from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, ProfileUpdateForm, ReviewForm
from .models import Cart, Customer, Menu, Order, OrderItem, Reservation, Review, Special

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
# reservation view now checks if user has a customer profile and shows it in the reservation form, and also handles reservation submission with messages
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

# authentication views for signup, login, logout, and profile management, using Django's built-in forms and authentication system, with added messages for user feedback
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# login view now sets session expiry to 7 days and redirects staff users to admin dashboard, with messages for invalid login attempts and successful logins, and also checks if user is already authenticated to redirect to home
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

# logout view simply logs out the user and redirects to home, no changes needed
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
# profile view now uses a custom form to allow users to update their profile information, and shows messages on successful update, with the form pre-filled with current user data
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
# settings page is a placeholder for future account settings, currently just shows a static page with a section variable for template use
def settings_page(request):
    return render(request, "web_app/account/settings.html", {"section": "settings"})


@login_required
# delete account view now requires POST method for security, and shows a confirmation page before deletion, with messages on successful deletion and redirects to home after logout
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("home")
    return render(request, "web_app/account/confirm_delete.html")

# reservation view now checks if user is authenticated to allow making a reservation, and also checks if user has a customer profile before allowing reservation submission, with messages for errors and success, and also passes customer profile to the template for pre-filling reservation form if available
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

# AJAX view to load more menu items for infinite scrolling on the menu page, returns JSON response with menu item data, and uses offset and limit parameters to paginate results
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
# AJAX view to add a menu item to the cart, expects POST data with menu_id and quantity, checks if the menu item is available, and creates or updates a Cart object for the user, returning a JSON response with a success message
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
# AJAX view to get current cart items for the logged-in user, returns a JSON response with a list of cart items including menu_id, name, quantity, and subtotal for each item, using select_related to optimize database queries
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

# AJAX view to remove a menu item from the cart, expects POST data with menu_id, checks if the cart item exists for the user and deletes it, returning a JSON response with a success message
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

# AJAX view to clear all items from the cart for the logged-in user, deletes all Cart objects for the user and returns a JSON response with a success message
@login_required
@require_POST
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return JsonResponse({"message": "cleared"})

# AJAX view to confirm an order, checks if the cart is not empty and if the user has a customer profile, creates an Order object with related OrderItems for each cart item, calculates the total price, and then clears the cart, returning a JSON response with a success message and a redirect URL to the user's orders page
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

# reservation view now checks if user is authenticated to allow making a reservation, and also checks if user has a customer profile before allowing reservation submission, with messages for errors and success, and also passes customer profile to the template for pre-filling reservation form if available
@login_required
def my_orders(request):
    customer, missing_response = get_customer_or_redirect(request, "home")
    if missing_response:
        return missing_response

    orders = Order.objects.filter(user=customer.user).prefetch_related("items__menu")
    return render(request, "web_app/main_page/my_orders.html", {"orders": orders})

# cancel order view now requires POST method for security, checks if the order belongs to the logged-in user, and shows a message that order cancellation is handled by staff in Django admin, then redirects back to the user's orders page
@login_required
@require_POST
def cancel_order(request, orderid):
    customer, missing_response = get_customer_or_redirect(request, "my_orders")
    if missing_response:
        return missing_response

    get_object_or_404(Order, pk=orderid, user=customer.user)
    messages.info(request, "Order cancellation is now handled by staff in Django admin.")
    return redirect("my_orders")

# account views for orders, reservations, and reviews, now check if the user has a customer profile and show messages if missing, and also use select_related to optimize database queries when fetching related data for display in the templates
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

# account reservations view now checks if user has a customer profile and shows it in the reservation form, and also handles reservation submission with messages, and also passes customer profile to the template for pre-filling reservation form if available, and uses select_related to optimize queries when fetching reservations for display in the template
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

# account reviews view now checks if user has a customer profile and shows it in the review form, and also handles review submission with messages, and also passes customer profile to the template for pre-filling review form if available, and uses select_related to optimize queries when fetching reviews for display in the template
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

# AJAX view to add a menu item review, expects POST data with menu_id, rating, and optional comment, checks if the user has a customer profile, and creates or updates a Review object for the user and menu item, returning a JSON response with a success message, and also uses update_or_create to handle both creating new reviews and updating existing ones in one query
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

# AJAX view to add a restaurant review, expects POST data with rating and optional comment, checks if the user has a customer profile, and creates or updates a Review object for the user with menu set to None to indicate it's a restaurant review, returning a JSON response with a success message, and also uses update_or_create to handle both creating new reviews and updating existing ones in one query
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

# view to display all reviews, now separates menu item reviews and restaurant reviews, and uses select_related to optimize queries when fetching related user and menu data for display in the template
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

# view to edit a review, checks if the review belongs to the logged-in user, and allows editing the rating and comment using a form, with messages on successful update, and also pre-fills the form with current review data for convenience
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
