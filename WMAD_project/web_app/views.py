from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileUpdateForm
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import redirect, get_object_or_404

from .models import Cart, CartItem, Order, OrderContain, Menu


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



#order  page logic
# web_app/views.py


# order PAGE (load first 8 items)

def order(request):
    items = Menu.objects.all()[:8]
    total_menu_count = Menu.objects.count()
    return render(request, 'web_app/main_page/order.html', {
        "items": items,
        "total_items": total_menu_count,
    })



# load more items

def load_more_menu(request):
    offset = int(request.GET.get("offset", 0))
    limit = 8
    items = list(Menu.objects.all()[offset:offset + limit].values())

    return JsonResponse({"items": items})



# add to cart


@login_required
def add_to_cart(request):

    menu_id = request.POST.get("menu_id")
    if not menu_id or not menu_id.isdigit():
      return JsonResponse({"error": "Invalid menu id"}, status=400)
    
    qty = int(request.POST.get("quantity", 1))
    if qty < 1:
      return JsonResponse({"error": "Invalid quantity"}, status=400)
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        qty = int(request.POST.get("quantity", 1))

        menu_item = get_object_or_404(Menu, menuID=menu_id)

        
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu=menu_item,
            defaults={"quantity": qty, "unit_price": menu_item.price}
        )

        if not created:
            cart_item.quantity += qty
            cart_item.save()

        return JsonResponse({"message": "Added to cart!"})

    return JsonResponse({"error": "Invalid request"}, status=400)



# get cartitem,js refresh)

def get_cart_items(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = [{
        "menuID": ci.menu.menuID,       
        "name": ci.menu.menuName,       
        
       
        "qty": ci.quantity,
        "subtotal": float(ci.subtotal()),
    } for ci in cart.cartitem_set.all()]

    return JsonResponse({"items": items})


#orderdelete



@login_required
@require_POST
def remove_from_cart(request):
    menu_id = request.POST.get("menu_id")
    if not menu_id:
        return JsonResponse({"error": "menu_id required"}, status=400)

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return JsonResponse({"error": "Cart not found"}, status=404)

    cart_item = cart.cartitem_set.filter(menu__menuID=menu_id).first()
    if not cart_item:
        return JsonResponse({"error": "Item not found"}, status=404)

    cart_item.delete()
    return JsonResponse({"message": "Item removed"})


# views.py

#forclearingcart



@login_required
@require_POST
def clear_cart(request):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Delete all CartItems linked to this cart
    cart.cartitem_set.all().delete()

    return JsonResponse({"message": "Cart cleared"})






@login_required
@require_POST
def confirm_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()

    if not items.exists():
        return JsonResponse({"error": "Cart is empty. Cannot place order."}, status=400)

    delivery_mode = request.POST.get("delivery_mode", "")
    if delivery_mode == "pickup":   
       delivery_address = "NONE"
    elif delivery_mode == "dinein":
        delivery_address = "NONE"

    elif delivery_mode == "":   
       
       return JsonResponse({"error": "Please enter an order option."}, status=400)
    
    else:
        delivery_address = request.POST.get("delivery_address", "").strip()
    
    
    
    
    
        

    

    order = Order.objects.create(
        customer=request.user,
        totalamount=cart.total_amount(),
        ordertype=delivery_mode,
        deliveryaddress=delivery_address,
        
    )

    for item in items:
        OrderContain.objects.create(
            order=order,
            menu=item.menu,
            quantity=item.quantity,
            unitprice=item.unit_price
        )

    items.delete()
    return JsonResponse({"message": "Order confirmed"})


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-order_date', '-order_time')
    return render(request, "web_app/main_page/my_orders.html", {"orders": orders})


@login_required()
@require_POST
def cancel_order(request, orderid):
    order = get_object_or_404(Order, orderid=orderid, customer=request.user)
    if order.status == "completed":
        return JsonResponse({"error": "Completed orders cannot be cancelled."}, status=400)
    
    order.status = "cancelled"  
    order.save()
    return redirect("my_orders")
 

