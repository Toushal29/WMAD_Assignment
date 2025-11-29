# C:\Users\toush\Desktop\WMAD_Assignment\WMAD_project\control_panel\views.py

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
import logging
import sys
import os
from datetime import datetime

logger = logging.getLogger('control_panel')

# """Dashboard — Logs access to control panel."""
def dashboard(request):
    ip = request.META.get('REMOTE_ADDR')
    user = request.user.username if request.user.is_authenticated else "anonymous"
    logger.info(f"Control panel viewed by IP {ip} (user: {user})")
    running = 'runserver' in sys.argv
    maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)
    return render(request, 'control_panel/dashboard.html', {
        'restaurant_name': 'Saveur Moris',
        'server_running': running,
        'maintenance_mode': maintenance_mode,
    })

# """Secure toggle — requires super password + logs events + sends email."""
def toggle_maintenance(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    # Extract inputs
    super_password = request.POST.get('super_password')
    correct_password = settings.SUPER_MAINTENANCE_PASSWORD
    ip = request.META.get('REMOTE_ADDR')
    user = request.user.username if request.user.is_authenticated else "anonymous"
    # Password check
    if super_password != correct_password:
        logger.info(f"FAILED SUPER PASSWORD attempt from IP {ip}")
        return JsonResponse({'error': 'Invalid super password'}, status=403)
    previous_state = getattr(settings, 'MAINTENANCE_MODE', False)
    new_state = not previous_state
    settings.MAINTENANCE_MODE = new_state
    # Log event
    logger.info(
        f"Maintenance mode {'ACTIVATED' if new_state else 'DEACTIVATED'} "
        f"by IP {ip} (user: {user})"
    )
    # Prepare email
    action = "ACTIVATED" if new_state else "DEACTIVATED"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"[Saveur Moris] Maintenance Mode {action}"
    message = (
        f"Maintenance mode was {action}.\n\n"
        f"Date/Time: {now}\n"
        f"By User: {user}\n"
        f"IP Address: {ip}\n"
    )
    try:
        send_mail(
            subject,
            message,
            "no-reply@saveurmoris.com",
            settings.MAINTENANCE_ALERT_EMAILS,
            fail_silently=False,
        )
        logger.info(f"Notification email sent to: {settings.MAINTENANCE_ALERT_EMAILS}")
    except Exception as e:
        logger.info(f"EMAIL ERROR: {str(e)}")
    return JsonResponse({'status': f'Maintenance mode toggled to {new_state}'})

# """Display logs in UI."""
def view_logs(request):
    
    log_file_path = os.path.join(settings.BASE_DIR, 'control_panel.log')
    logs = []
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()[-1000:]  # limit to last 1000 lines
    return render(request, 'control_panel/logs.html', {'logs': logs})
