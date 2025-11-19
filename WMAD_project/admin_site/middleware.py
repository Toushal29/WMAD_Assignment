# this will ensure that only authenticated admin users can access the admin site views and not login to regular site views

from django.conf import settings

class AdminSiteSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # If the request is for admin-site, use custom cookie name
        if request.path.startswith("/admin-site/"):
            settings.SESSION_COOKIE_NAME = "admin_sessionid"
        else:
            settings.SESSION_COOKIE_NAME = "sessionid"

        return self.get_response(request)
