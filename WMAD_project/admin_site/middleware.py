# this will ensure that only authenticated admin users can access the admin site views and not login to regular site views
from django.utils.deprecation import MiddlewareMixin

class AdminSiteSessionMiddleware(MiddlewareMixin):

    def process_response(self, request, response):

        # admin-site uses separate cookie
        if request.path.startswith("/admin-site/"):
            response.set_cookie(
                "admin_sessionid",
                request.session.session_key,
                max_age=60 * 60 * 24 * 7,  # 7 days
                httponly=True,
                samesite="Lax"
            )

        return response
