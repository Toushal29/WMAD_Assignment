from django.contrib import admin
from .models import Users, Admin, Customer, Menu, Reservation, Cart, CartItem, Order, OrderContain,  Reviews

# Register your models here.
admin.site.register(Users)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Reservation)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderContain)

admin.site.register(Reviews)
