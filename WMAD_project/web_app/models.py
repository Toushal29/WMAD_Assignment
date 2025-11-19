from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[ ('admin', 'Admin'), ('customer', 'Customer')],
        default='customer'
    )
    def __str__(self):
        return self.username

class Admin(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    admin_name = models.CharField(max_length=100)

    def __str__(self):
        return self.admin_name

class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
