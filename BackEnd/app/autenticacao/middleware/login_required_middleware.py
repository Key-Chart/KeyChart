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
            # Permitir acesso público às rotas de inscrições online
            if (request.path not in self.public_paths and 
                not request.path.startswith('/static/') and
                not request.path.startswith('/inscricoes/') and
                not request.path.startswith('/media/')):
                return redirect('login')
        return self.get_response(request)
