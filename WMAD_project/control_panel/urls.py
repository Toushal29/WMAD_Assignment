from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('maintenance/toggle/', views.toggle_maintenance, name='toggle_maintenance'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_app.urls')),  # include your app URLs
]
