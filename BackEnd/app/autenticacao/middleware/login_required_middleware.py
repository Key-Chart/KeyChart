from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            '/keychart/login/', '/keychart/password_reset/', '/keychart/logout/', '/static/', '/inscricoes/', '/portal-atleta/'
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(p) for p in self.public_paths):
                return redirect('login')
        return self.get_response(request)
