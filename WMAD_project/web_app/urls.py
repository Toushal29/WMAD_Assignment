# C:\Users\toush\Desktop\WMAD_Assignment\WMAD_project\web_app\urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # MAIN PAGES
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservation/', views.reservation, name='reservation'),
    path('about-contact/', views.about_contact, name='about_contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    # SIMPLE AUTH (entry folder)
    path('login/', views.user_login, name='simple_login'),
    path('signup/', views.user_signup, name='simple_signup'),
    # ACCOUNT (Django Auth Forms)
    path('account/login/', views.login_view, name='login'),
    path('account/signup/', views.signup, name='signup'),

    path('profile/', views.profile_page, name='profile'),
    path('profile/settings/', views.settings_page, name='settings'),
    path('profile/my_orders/', views.orders_page, name='orders'),
    path('profile/my_reviews/', views.reviews_page, name='reviews'),

    path('account/logout/', views.logout_view, name='logout'),
    path('account/delete/', views.delete_account, name='delete_account'),
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
    # AJAX / CART / ORDER SYSTEM
    path('ajax/load-more/', views.load_more_menu, name='load_more'),
    path('ajax/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('ajax/get-cart/', views.get_cart_items, name='get_cart'),
    path('ajax/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('ajax/clear-cart/', views.clear_cart, name='clear_cart'),
    path('ajax/confirm-order/', views.confirm_order, name='confirm_order'),

    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:orderid>/', views.cancel_order, name='cancel_order'),
]