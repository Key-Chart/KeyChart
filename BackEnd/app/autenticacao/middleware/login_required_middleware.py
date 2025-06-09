from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            reverse('login'),
            reverse('logout'),
        ]

    def __call__(self, request):
        if not request.session.get('usuario_autenticado'):
            if request.path not in self.public_paths and not request.path.startswith('/static/'):
                return redirect('login')
        return self.get_response(request)
