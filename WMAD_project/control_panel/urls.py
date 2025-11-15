from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('maintenance/toggle/', views.toggle_maintenance, name='toggle_maintenance'),
    path('logs/', views.view_logs, name='view_logs'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
