from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.conf import settings
# USERS / ADMIN / CUSTOMER
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

# MENU
class Menu(models.Model):
    menuID = models.AutoField(primary_key=True)
    menuName = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.ImageField(upload_to='menu_images/')   # static files, so no ImageField

    def __str__(self):
        return self.menuName

# RESERVATION
class Reservation(models.Model):
    reservationID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.customer.user.username} - {self.reservation_date} {self.reservation_time}"

# ORDER (Placed by customer)
# a cart  belongs to a user

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def total_amount(self):
        return sum(item.subtotal() for item in self.cartitem_set.all())



# cartitem
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def subtotal(self):
        return self.unit_price * self.quantity



# order
class Order(models.Model):
    ORDER_TYPES = (
        ("pickup", "Pickup"),
        ("dinein", "Dine-IN"),
        ("delivery", "Delivery"),
    )
    
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    orderid = models.AutoField(primary_key=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Separate fields
    order_date = models.DateField(auto_now_add=True)   
    order_time = models.TimeField(auto_now_add=True)   

    totalamount = models.DecimalField(max_digits=10, decimal_places=2)
    ordertype = models.CharField(max_length=20, choices=ORDER_TYPES)
    deliveryaddress = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending")

    def __str__(self):
        return f"Order #{self.orderid}"



# order items

class OrderContain(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unitprice = models.DecimalField(max_digits=6, decimal_places=2)


# REVIEWS
# Supports:
# - Restaurant reviews
# - Menu item reviews
class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_restaurant_review(self):
        return self.menu is None

    def __str__(self):
        return f"Review {self.review_id} - {self.customer.user.username}"
# Crfrom django.db import models

class Special(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available_days = models.CharField(default='Monday–Sunday', max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    image = models.ImageField(upload_to='specials/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

