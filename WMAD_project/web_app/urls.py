from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('reservation/', views.reservation, name='reservation'),
    path('about-contact/', views.about_contact, name='about_contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    ##all login
    path('account/login/', views.login_view, name='login'),

    ##custom signup view
    path('account/signup/', views.signup, name='signup'),       

    ##all after login
    path('profile/', views.profile_page, name='profile'),
    path('profile/settings/', views.settings_page, name='settings'),
    path('profile/my_orders/', views.orders_page, name='orders'),
    path('profile/my_reviews/', views.reviews_page, name='reviews'),

    ##all logout
    path('account/logout/', views.logout_view, name='logout'),
    # request reset link (enter email)
    path(
        'account/reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/custom_reset_request.html',
            email_template_name='registration/custom_reset_email.txt',   # ← ADD THIS
            html_email_template_name='registration/custom_reset_email.html',
            subject_template_name='registration/custom_reset_subject.txt',
            success_url='/account/reset-password/sent/',
        ),
        name='custom_reset_request'
    ),

    # email sent page
    path(
        'account/reset-password/sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/custom_reset_sent.html'
        ),
        name='custom_reset_sent'
    ),

    # link from email → set new password
    path(
        'account/reset-password/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/custom_reset_confirm.html',
            success_url='/account/reset-password/complete/',
        ),
        name='custom_reset_confirm'
    ),

    # password reset complete
    path(
        'account/reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/custom_reset_complete.html'
        ),
        name='custom_reset_complete'
    ),
]