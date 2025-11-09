from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservation/', views.reservation, name='reservation'),
    path('about-contact/', views.about_contact, name='about_contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('account/signup/', views.signup, name='signup'),       # custom signup view
]