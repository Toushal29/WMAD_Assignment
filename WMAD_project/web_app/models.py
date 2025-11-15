from django.db import models

# Crfrom django.db import models

class Special(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available_days = models.CharField(max_length=100, default='Monday–Sunday')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='specials/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)  # optional
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
