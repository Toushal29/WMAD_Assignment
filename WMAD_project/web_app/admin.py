from django.contrib import admin

# Regfrom django.contrib import admin
from django.contrib import admin
from .models import Special

admin.site.register(Special)

from django.contrib import admin
from .models import MenuItem

admin.site.register(MenuItem)
