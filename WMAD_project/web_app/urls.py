# C:\Users\...\WMAD_Assignment\WMAD_project\web_app\urls.py

# this file defines the URL patterns for the web application, mapping URLs to their corresponding view functions. It includes routes for main pages, user authentication, profile management, password reset/change, AJAX API endpoints for cart and orders, and review management.

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
        # API ENDPOINTS

    # This provides the login endpoint automatically
    path('api/auth/login/', obtain_auth_token, name='api_token_auth'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    
    path('api/auth/register/', views.api_register, name='api_register'),

    path('api/profile/<int:pk>/', views.api_profile, name='api_profile'),
    path('api/upd_profile/<int:pk>/', views.api_upd_profile, name='api_upd_profile'),
    path('api/profile/<int:pk>/delete/', views.api_delete_profile, name='api_delete_profile'),

    path('api/menus/', views.api_menus, name='api_menus'),
    path('api/menu/<int:pk>/', views.api_menu_detail, name='api_menu_detail'),

    path('api/customers/', views.api_customers, name='api_customers'),

    path('api/my-reviews/', views.api_my_reviews, name='api_my_reviews'),
    path('api/reviews/<int:review_id>/', views.api_upd_reviews, name='api_upd_reviews'),
    path('api/reviews/<int:review_id>/delete/', views.api_delete_reviews, name='api_delete_reviews'),

    path('api/my-reservations/', views.api_reservation_list, name='api_reservation_list'),
    path('api/my-reservations/<int:resev_id>/delete/', views.api_del_reservation, name='api_del_reservation'),
    path('api/reservations/create/', views.api_create_reservation, name='api_create_reservation'),

    path('api/my-orders/', views.api_order_list, name='api_order_list'),
    path('api/orders/<int:order_id>/items/', views.api_order_items, name='api_order_items'),
    path('api/orders/<int:order_id>/cancel/', views.api_cancel_order, name='api_cancel_order'),
    path('api/orders/preview/', views.api_checkout_preview, name='api_checkout_preview'),
    path('api/orders/place/', views.api_place_order, name='api_place_order'),






    # MAIN PAGES
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('checkout/', views.checkout, name='checkout'),
    path('about-contact/', views.about_contact, name='about_contact'),
    path('reservation/', views.reservation, name='reservation'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    # PUBLIC REVIEWS
    path("reviews/", views.view_reviews, name="reviews"),
    path("review/restaurant/add/", views.add_restaurant_review, name="add_restaurant_review"),

    # SIMPLE LOGIN/SIGNUP
    path('login/', views.login_view, name='simple_login'),
    path('signup/', views.signup, name='simple_signup'),

    # ACCOUNT LINKS
    path('account/login/', views.login_view, name='login'),
    path('account/signup/', views.signup, name='signup'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/delete/', views.delete_account, name='delete_account'),

    # PROFILE SECTIONS
    path('profile/', views.profile_page, name='profile'),
    path('profile/settings/', views.settings_page, name='settings'),
    path('profile/my_orders/', views.account_orders, name='orders'),
    # Add this to your urlpatterns
    path('order/cancel-action/<int:order_id>/', views.cancel_order_action, name='cancel_order_action'),
    path('profile/my_reservations/', views.account_reservations, name='reservations'),
    path('reservation/cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('profile/my_reviews/', views.account_reviews, name='account_reviews'),

    # PASSWORD RESET
    path(
        'account/reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/custom_reset_request.html',
            email_template_name='registration/custom_reset_email.txt',
            html_email_template_name='registration/custom_reset_email.html',
            subject_template_name='registration/custom_reset_subject.txt',
            success_url='/account/reset-password/sent/',
        ),
        name='custom_reset_request'
    ),

    path(
        'account/reset-password/sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/custom_reset_sent.html'
        ),
        name='custom_reset_sent'
    ),

    path(
        'account/reset-password/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/custom_reset_confirm.html',
            success_url='/account/reset-password/complete/',
        ),
        name='custom_reset_confirm'
    ),

    path(
        'account/reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/custom_reset_complete.html'
        ),
        name='custom_reset_complete'
    ),

    # PASSWORD CHANGE
    path(
        'account/change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/custom_change_password.html',
            success_url='/account/change-password/done/',
        ),
        name='custom_change_password'
    ),

    path(
        'account/change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/custom_change_password_done.html'
        ),
        name='custom_change_password_done'
    ),

    # AJAX CART / ORDER API
    path('ajax/load-more/', views.load_more_menu, name='load_more'),
    path('ajax/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('ajax/get-cart/', views.get_cart_items, name='get_cart'),
    path('ajax/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('ajax/clear-cart/', views.clear_cart, name='clear_cart'),
    path('ajax/confirm-order/', views.confirm_order, name='confirm_order'),

    # MY ORDERS PAGE
    path('my-orders/', views.my_orders, name='my_orders'),

    # REVIEWS
    path("review/add/<int:menu_id>/", views.add_review, name="add_review"),

    # EDIT / DELETE
    path("review/edit/<int:review_id>/", views.edit_review, name="edit_review"),
    path("review/delete/<int:review_id>/", views.delete_review, name="delete_review"),
]
