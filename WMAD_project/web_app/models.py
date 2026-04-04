from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Menu(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    detail_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="menu_images/")
    category = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Special(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available_days = models.CharField(max_length=100, default="Monday-Sunday")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="specials/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    SEATING_INDOOR = "Indoor"
    SEATING_OUTDOOR = "Outdoor"

    SEATING_CHOICES = [
        (SEATING_INDOOR, "Indoor"),
        (SEATING_OUTDOOR, "Outdoor"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField(default=1)
    seating_choice = models.CharField(
        max_length=20,
        choices=SEATING_CHOICES,
        default=SEATING_INDOOR,
    )
    allergy_info = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    class Meta:
        ordering = ["-reservation_date", "-reservation_time"]

    def __str__(self):
        return f"{self.customer.user.username} - {self.reservation_date} {self.reservation_time}"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menu"],
                name="unique_cart_item_per_user_menu",
            )
        ]
        ordering = ["-added_at"]

    @property
    def line_total(self):
        return self.menu.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.menu.name} x {self.quantity}"


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PREPARING = "preparing"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PREPARING, "Preparing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-order_date"]

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.order_id} - {self.menu.name} x {self.quantity}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        target = self.menu.name if self.menu else "Restaurant"
        return f"{self.user.username} - {target} ({self.rating}/5)"
