# C:\...\WMAD_project\admin_site\urls.py

from django.urls import path
from . import views

urlpatterns = [

    # AUTH
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # DASHBOARD
    path('', views.admin_dashboard, name='admin_dashboard'),

    # MENU MANAGEMENT
    path('edit-menu/', views.edit_menu_page, name='admin_edit_menu'),
    path('edit-menu/add/', views.admin_add_menu, name='admin_add_menu'),
    path('edit-menu/<int:id>/update/', views.admin_update_menu, name='admin_update_menu'),
    path('edit-menu/<int:id>/delete/', views.admin_delete_menu, name='admin_delete_menu'),

    # CUSTOMER MANAGEMENT
    path('customers/', views.customer_details_page, name='admin_customer_details'),
    path('customers/<int:id>/edit/', views.customer_edit, name='admin_customer_edit'),
    path('customers/<int:id>/update/', views.customer_update, name='admin_customer_update'),
    path('customers/<int:id>/delete/', views.customer_delete, name='admin_customer_delete'),

    # FEEDBACK
    path('feedback/', views.feedback_page, name='admin_feedback'),

    # RESERVATIONS
    path('reservation/', views.reservation_page, name='admin_reservation'),
    path('reservation/<int:id>/edit/', views.reservation_edit, name='admin_reservation_edit'),
    path('reservation/<int:id>/update/', views.reservation_update, name='admin_reservation_update'),
    path('reservation/<int:id>/delete/', views.reservation_delete, name='admin_reservation_delete'),

    # ORDER MANAGEMENT PAGE
    path('orders/', views.orders_page, name='admin_orders'),

    # AJAX ACTIONS
    path('ajax/order-complete/', views.complete_order, name='complete_order'),
    path('ajax/order-cancel/', views.admin_cancel_order, name='admin_cancel_order'),
]
