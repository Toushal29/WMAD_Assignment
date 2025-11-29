# C:\Users\toush\Desktop\WMAD_Assignment\WMAD_project\web_app\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# ============================
# CUSTOM USER
# ============================

class Users(AbstractUser):
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('customer', 'Customer')],
        default='customer'
    )

    def __str__(self):
        return self.username


class Admin(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


# ============================
# MENU + SPECIALS
# ============================

class Menu(models.Model):
    menuID = models.AutoField(primary_key=True)
    menuName = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.menuName


class Special(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available_days = models.CharField(max_length=100, default='Monday–Sunday')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='specials/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ============================
# RESERVATION
# ============================

class Reservation(models.Model):
    reservationID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )

    def __str__(self):
        return f"{self.customer.user.username} - {self.reservation_date}"


# ============================
# CART SYSTEM
# ============================

class Cart(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)

    def total_amount(self):
        return sum(item.subtotal for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


# ============================
# ORDER SYSTEM
# ============================

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    orderID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Users, on_delete=models.CASCADE)

    # new field added
    order_type = models.CharField(max_length=20, default="pickup")

    # FIX: deliveryaddress should allow blank for dine-in/pickup
    deliveryaddress = models.CharField(max_length=255, blank=True, null=True)

    totalamount = models.DecimalField(max_digits=10, decimal_places=2)

    # Existing
    order_date = models.DateTimeField(auto_now_add=True)

    # NEW FIELD: order_time (admin panel expects this)
    order_time = models.TimeField(auto_now_add=True)

    # NEW FIELD: status (admin panel uses this everywhere)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return f"Order #{self.orderID}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.menu.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu.menuName} x {self.quantity}"


# ============================
# REVIEWS
# ============================

class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id}"
