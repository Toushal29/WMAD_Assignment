from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Cart, Customer, Menu, Order, OrderItem, Reservation, Review, Special


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = True
    extra = 0


class CustomUserAdmin(BaseUserAdmin):
    inlines = [CustomerInline]


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "created_at")
    search_fields = ("user__username", "user__email", "phone", "address")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "available")
    list_filter = ("available", "category")
    search_fields = ("name", "description", "detail_description", "category")


@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "available_days", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "available_days")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "reservation_date",
        "reservation_time",
        "party_size",
        "status",
    )
    list_filter = ("status", "reservation_date", "seating_choice")
    search_fields = ("customer__user__username", "customer__phone", "allergy_info")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "menu", "quantity", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__username", "menu__name")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "order_date")
    list_filter = ("status", "order_date")
    search_fields = ("user__username", "user__email")
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "menu", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "menu__name", "comment")
