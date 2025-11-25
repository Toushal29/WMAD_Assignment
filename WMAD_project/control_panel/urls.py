from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('maintenance/toggle/', views.toggle_maintenance, name='toggle_maintenance'),
]