from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservation/', views.reservation, name='reservation'),
    path('about-contact/', views.about_contact, name='about_contact'),
      # web_app/urls.py
     path('login/', views.user_login, name='login'), 
    path('signup/', views.user_signup, name='signup'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('account/login/', views.login_view, name='login'),
    path('account/signup/', views.signup, name='signup'),       
    path('profile/', views.profile_page, name='profile'),
    path('profile/settings/', views.settings_page, name='settings'),
    path('profile/my_orders/', views.orders_page, name='orders'),
    path('profile/my_reviews/', views.reviews_page, name='reviews'),
    path('account/logout/', views.logout_view, name='logout'),
    path('account/delete/', views.delete_account, name='delete_account'),
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
    # Change password (user must be logged in)
    path(
        'account/change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/custom_change_password.html',
            success_url='/account/change-password/done/',
        ),
        name='custom_change_password'
    ),

    # Change password done
    path(
        'account/change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/custom_change_password_done.html'
        ),
        name='custom_change_password_done'
    ),
]