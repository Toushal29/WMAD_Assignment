from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('customer', 'Customer')],
        default='customer'
    )

    
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def str(self):
        return self.username


class Admin(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    admin_name = models.CharField(max_length=100)

    def str(self):
        return self.admin_name


class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)

    def str(self):
        return self.user.username



class Menu(models.Model):
    menuID = models.AutoField(primary_key=True)
    menuName = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(max_length=255, null=True, blank=True)

    def str(self):
        return self.menuName


class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()

    def str(self):
        return f"Review {self.review_id} by {self.customer}"


class Reservation(models.Model):
    reservationID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    party_size = models.IntegerField()
    reservation_date = models.DateTimeField()
    status = models.CharField(max_length=50)

    def str(self):
        return f"Reservation {self.reservationID}"


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=50)  # e.g. Delivery / Dine-in
    delivery_addr = models.CharField(max_length=255, null=True, blank=True)

    def str(self):
        return f"Order {self.orderID}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menu')

    def str(self):
        return f"{self.quantity} x {self.menu.menuName}"