from django.contrib import admin
from web_app.models import (
    Users, Admin, Customer, Menu, Special, Reservation,
    Cart, CartItem, Order, OrderItem, Reviews
)

admin.site.register(Users)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Special)
admin.site.register(Reservation)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reviews)
