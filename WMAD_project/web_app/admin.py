from django.contrib import admin
from .models import Special, MenuItem, Reservation, Customer

admin.site.register(Special)
admin.site.register(MenuItem)
admin.site.register(Reservation)
admin.site.register(Customer)
