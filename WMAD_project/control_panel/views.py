from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os
import sys

def toggle_maintenance(request):
    if request.method == 'POST':
        settings.MAINTENANCE_MODE = not getattr(settings, 'MAINTENANCE_MODE', False)
        return JsonResponse({'status': 'Maintenance mode set to {}'.format(settings.MAINTENANCE_MODE)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def dashboard(request):
    running = 'runserver' in sys.argv
    maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)
    log_file = os.path.join(settings.BASE_DIR, 'debug.log')
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = f.readlines()[-50:]  # Show last 50 lines
    return render(request, 'control_panel/dashboard.html', {
        'restaurant_name': 'Saveur Moris',
        'server_running': running,
        'maintenance_mode': maintenance_mode,
        'logs': logs
    })