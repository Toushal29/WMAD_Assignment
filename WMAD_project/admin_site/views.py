from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from django.views.decorators.http import require_POST

from web_app.models import (
    Users,
    Customer,
    Reservation,
    Menu,
    Order,
    Reviews,
    Cart,
    CartItem,
    OrderItem,
)

def redirect_to_reservation(request):
    return redirect("admin_reservation")

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("admin_login")

        if not request.user.username.startswith("admin_"):
            return redirect("admin_login")

        if not (request.user.is_superuser or request.user.role == "admin"):
            return redirect("admin_login")

        request.admin_user = request.user
        return view_func(request, *args, **kwargs)

    return wrapper

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username").strip()
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        valid_username = username.startswith("admin_")

        if user and valid_username and (user.is_superuser or user.role == "admin"):
            login(request, user)
            request.session.set_expiry(86400 * 7)
            return redirect("admin_dashboard")

        messages.error(request, "Invalid admin credentials.")

    return redirect("admin_reservation")


def admin_logout(request):
    logout(request)
    return redirect("admin_login")

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
def reservation_edit(request, id):
    reservation = Reservation.objects.select_related("customer__user").filter(reservationID=id).first()

    if not reservation:
        messages.error(request, "Reservation not found.")
        return redirect("admin_reservation")

    return render(
        request,
        "admin_site/reservation_edit.html",
        {
            "active_tab": "reservation",
            "admin_user": request.admin_user,
            "reservation": reservation,
        }
    )

@admin_required
def reservation_update(request, id):
    reservation = Reservation.objects.select_related("customer__user").filter(reservationID=id).first()

    if not reservation:
        messages.error(request, "Reservation not found.")
        return redirect("admin_reservation")

    if request.method == "POST":

        if request.POST.get("reservation_date"):
            reservation.reservation_date = request.POST["reservation_date"]

        if request.POST.get("reservation_time"):
            reservation.reservation_time = request.POST["reservation_time"]

        if request.POST.get("party_size"):
            reservation.party_size = request.POST["party_size"]

        if request.POST.get("status"):
            reservation.status = request.POST["status"]

        if request.POST.get("seating_choice"):
            reservation.seating_choice = request.POST["seating_choice"]

        if request.POST.get("allergy_info"):
            reservation.allergy_info = request.POST["allergy_info"]

        reservation.save()
        messages.success(request, "Reservation updated.")
        return redirect("admin_reservation")

    return redirect("admin_reservation")

@admin_required
def reservation_delete(request, id):
    reservation = Reservation.objects.filter(reservationID=id).first()

    if not reservation:
        messages.error(request, "Reservation not found.")
        return redirect("admin_reservation")

    reservation.delete()
    messages.success(request, "Reservation deleted.")
    return redirect("admin_reservation")

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
def customer_edit(request, id):
    customer = Customer.objects.select_related("user").filter(user_id=id).first()

    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("admin_customer_details")

    return render(
        request,
        "admin_site/customer_edit.html",
        {
            "active_tab": "customer_details",
            "admin_user": request.admin_user,
            "customer": customer,
        }
    )

@admin_required
def customer_update(request, id):
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

    return redirect("admin_customer_details")

@admin_required
def customer_delete(request, id):
    customer = Customer.objects.filter(user_id=id).first()

    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("admin_customer_details")

    user = customer.user
    user.delete()

    messages.success(request, "Customer deleted successfully.")
    return redirect("admin_customer_details")

@admin_required
def customer_details_page(request):
    search = request.GET.get("search", "").strip()

    if search:
        customers = Customer.objects.select_related('user').filter(
            models.Q(user__first_name__icontains=search)
            | models.Q(user__last_name__icontains=search)
            | models.Q(user__email__icontains=search)
            | models.Q(user__username__icontains=search)
            | models.Q(user__phone_no__icontains=search)
            | models.Q(address__icontains=search)
        )
    else:
        customers = Customer.objects.select_related('user').all().order_by('-user_id')

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

@admin_required
def orders_page(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    status_filter = request.GET.get("status")

    orders = Order.objects.select_related("customer__user").order_by("-order_date")

    if start and end:
        orders = orders.filter(order_date__range=[start, end])

    if status_filter in ["pending", "completed", "cancelled"]:
        orders = orders.filter(status=status_filter)

    total_orders = orders.count()
    total_completed = orders.filter(status="completed").count()
    total_cancelled = orders.filter(status="cancelled").count()

    data = []
    for o in orders:
        data.append({
            "orderID": o.orderID,
            "customer": o.customer.user.username,
            "phone": o.customer.user.phone_no or "N/A",
            "address": "Sur place" if o.order_type in ["pickup", "dinein"] else o.deliveryaddress,
            "date": o.order_date.strftime("%Y-%m-%d %H:%M"),
            "total": o.totalamount,
            "status": o.status,
            "items": [
                {"name": item.menu.menuName, "quantity": item.quantity}
                for item in o.orderitem_set.all()
            ]
        })

    return render(request, "admin_site/orders.html", {
        "orders": data,
        "total_orders": total_orders,
        "total_delivered": total_completed,
        "total_cancelled": total_cancelled,
        "start": start or "",
        "end": end or "",
        "status_filter": status_filter or "",
    })

@admin_required
@require_POST
def complete_order(request):
    order_id = request.POST.get("order_id")

    order = Order.objects.filter(orderID=order_id).first()
    if not order:
        return JsonResponse({"success": False, "error": "Order not found"})

    order.status = "completed"
    order.save()

    return JsonResponse({"success": True})

@admin_required
@require_POST
def admin_cancel_order(request):
    order_id = request.POST.get("order_id")

    order = Order.objects.filter(orderID=order_id).first()
    if not order:
        return JsonResponse({"success": False})

    order.status = "cancelled"
    order.save()

    return JsonResponse({"success": True})

@admin_required
def admin_add_menu(request):
    if request.method == "POST":
        Menu.objects.create(
            menuName=request.POST.get("menuName"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            image_url=request.FILES.get("image_url"),
        )
        messages.success(request, "Menu item added.")
    return redirect("admin_edit_menu")

@admin_required
def admin_update_menu(request, id):
    item = Menu.objects.filter(menuID=id).first()

    if not item:
        messages.error(request, "Menu item not found.")
        return redirect("admin_edit_menu")

    if request.method == "POST":
        item.menuName = request.POST.get("menuName", item.menuName)
        item.description = request.POST.get("description", item.description)
        item.price = request.POST.get("price", item.price)

        if request.FILES.get("image_url"):
            item.image_url = request.FILES["image_url"]

        item.save()
        messages.success(request, "Menu updated successfully.")

    return redirect("admin_edit_menu")

@admin_required
def admin_delete_menu(request, id):
    item = Menu.objects.filter(menuID=id).first()

    if item:
        item.delete()
        messages.success(request, "Menu item deleted.")

    return redirect("admin_edit_menu")
