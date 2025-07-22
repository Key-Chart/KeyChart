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
        # Ignorar completamente rotas do portal do atleta (controle de login próprio)
        if request.path.startswith('/portal-atleta/'):
            return self.get_response(request)
        # Permitir acesso se for usuário autenticado normal OU atleta autenticado
        if not (request.session.get('usuario_autenticado') or request.session.get('atleta_id')):
            # Permitir acesso público às rotas de inscrições online
            if (request.path not in self.public_paths and 
                not request.path.startswith('/static/') and
                not request.path.startswith('/inscricoes/') and
                not request.path.startswith('/media/') and
                not request.path.startswith('/portal-atleta/login') and
                not request.path.startswith('/portal-atleta/recuperar-senha')):
                return redirect('login')
        return self.get_response(request)
