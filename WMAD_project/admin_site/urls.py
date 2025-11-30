from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),

    path('', views.admin_dashboard, name='admin_dashboard'),
    path('edit-menu/', views.edit_menu_page, name='admin_edit_menu'),
    path('feedback/', views.feedback_page, name='admin_feedback'),
    path('customers/', views.customer_details_page, name='admin_customer_details'),
    path('customers/<int:id>/edit/', views.customer_edit, name='admin_customer_edit'),
    path('customers/<int:id>/update/', views.customer_update, name='admin_customer_update'),
    path('customers/<int:id>/delete/', views.customer_delete, name='admin_customer_delete'),
    path('edit-price/', views.edit_price_page, name='admin_edit_price'),
    path('orders/', views.orders_page, name='admin_orders'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('reservation/', views.reservation_page, name='admin_reservation'),
    path('reservation/<int:id>/edit/', views.reservation_edit, name='admin_reservation_edit'),
    path('reservation/<int:id>/update/', views.reservation_update, name='admin_reservation_update'),
    path('reservation/<int:id>/delete/', views.reservation_delete, name='admin_reservation_delete'),
]
