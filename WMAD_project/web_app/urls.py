from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservation/', views.reservation, name='reservation'),
    path('about-contact/', views.about_contact, name='about_contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]