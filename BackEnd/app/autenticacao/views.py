from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # Adicionado para mensagens
from django.contrib.auth import logout
from decouple import config

# Credenciais fixas vindas do .env
USUARIO_FIXO = config('USUARIO_FIXO')
SENHA_FIXA = config('SENHA_FIXA')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')

        if usuario == USUARIO_FIXO and senha == SENHA_FIXA:
            request.session['usuario_autenticado'] = True
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')  # Mensagem de erro
            return redirect('login')  # Redireciona de volta para a página de login

    return render(request, 'autenticacao/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')  # Mensagem de informação
    return redirect('login')