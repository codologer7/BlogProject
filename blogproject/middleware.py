"""
Middleware to fix ALLOWED_HOSTS issues on Vercel
"""

class VercelHostMiddleware:
    """Middleware to handle Vercel deployment domains"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get the host header
        host = request.get_host()
        
        # If running on Vercel (host ends with vercel.app), add it to ALLOWED_HOSTS
        if host.endswith('.vercel.app'):
            from django.conf import settings
            if host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append(host)
        
        response = self.get_response(request)
        return response
