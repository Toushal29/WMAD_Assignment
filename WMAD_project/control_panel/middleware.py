#for maintenance mode

from django.conf import settings            # for accessing settings
from django.shortcuts import render         # for rendering templates

class MaintenanceMiddleware:                # custom middleware class for maintenance mode
    def __init__(self, get_response):       # initialization method
        self.get_response = get_response    # store the get_response callable

    def __call__(self, request):                            # check if the request path starts with '/control/'
        if request.path.startswith('/control/'):            # if so, allow access to control panel views
            return self.get_response(request)               # proceed to the next middleware or view
        if getattr(settings, 'MAINTENANCE_MODE', False):    # check if maintenance mode is enabled in settings
            return render(request, 'control_panel/customer_maintenance.html', {'status': 'Website Under Maintenance'})                                  # render maintenance page
        return self.get_response(request)                   # proceed to the next middleware or view if not in maintenance mode