from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservation/', views.reservation, name='reservation'),
    path('about-contact/', views.about_contact, name='about_contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    ##all login
    path('account/login/', views.login_view, name='login'),
    path('account/signup/', views.signup, name='signup'),       ##custom signup view
    ##all after login
    path('profile/', views.profile_page, name='profile'),
    path('profile/settings/', views.settings_page, name='settings'),
    path('profile/my_orders/', views.orders_page, name='orders'),
    path('profile/my_reviews/', views.reviews_page, name='reviews'),
    ##all logout
    path('account/logout/', views.logout_view, name='logout'),
]