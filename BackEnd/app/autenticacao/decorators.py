from django.shortcuts import redirect

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('login')  # Altere pro nome da sua rota de login
        return view_func(request, *args, **kwargs)
    return wrapper
