from django.urls import path
from . import views

app_name = 'accounts'  # ← THIS IS IMPORTANT

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # API endpoints
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/my-profile/', views.api_my_profile, name='api_profile'),
    path('api/test/', views.api_test, name='api_test'),
]