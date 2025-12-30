"""
Custom middleware for Renovation Tracker
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse


class AdminRedirectMiddleware:
    """
    Redirect admin URLs for disabled models to custom modern forms.
    This provides a better UX than showing 404 errors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Map admin paths to custom form URLs
        self.redirect_map = {
            '/admin/renovation/purchase/add/': 'purchase_add',
            '/admin/renovation/worksession/add/': 'session_add',
            '/admin/renovation/roomprogress/add/': 'progress_add',
        }

    def __call__(self, request):
        # Check if the request path matches any disabled admin URLs
        for admin_path, view_name in self.redirect_map.items():
            if admin_path in request.path:
                # Add a helpful message
                messages.info(
                    request,
                    _('Panel administracyjny dla tego modelu został wyłączony. Użyj nowoczesnego formularza poniżej.')
                )
                # Redirect to the modern form
                return redirect(view_name)

        response = self.get_response(request)
        return response
