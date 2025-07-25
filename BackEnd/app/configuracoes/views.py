from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
import random
from django.core.mail import send_mail
from .models import CodigoVerificacao
from django.template.loader import render_to_string

User = get_user_model()

MASTER_PASSWORD = getattr(settings, 'MASTER_PASSWORD', 'senha123')

def configuracoes(request):
    if request.method == 'POST':
        if request.POST.get('master_auth'):
            senha = request.POST.get('master_senha')
            if senha == MASTER_PASSWORD:
                request.session['master_authenticated'] = True
                messages.success(request, 'Autenticação realizada com sucesso!')
            else:
                messages.error(request, 'Senha master incorreta! Por favor, tente novamente.')
                return render(request, 'configuracoes/configuracoes.html', {'usuarios': User.objects.all()})
        elif not request.session.get('master_authenticated'):
            messages.error(request, 'Autentique-se como chefe do sistema para editar usuários.')
            return render(request, 'configuracoes/configuracoes.html', {'usuarios': User.objects.all()})
        elif request.POST.get('add_user'):
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            perfil = request.POST.get('perfil')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Já existe um usuário com esse email.')
            else:
                codigo_verificacao = str(random.randint(100000, 999999))
                user = User.objects.create_user(username=email, email=email, password=senha, is_active=False)
                user.first_name = nome
                user.save()
                CodigoVerificacao.objects.create(user=user, codigo=codigo_verificacao)
                email_html = render_to_string('configuracoes/emails/verificacao.html', {
                    'nome': nome,
                    'codigo': codigo_verificacao,
                })
                send_mail(
                    'Verifique seu acesso ao KeyChart',
                    f'Seu código de verificação é: {codigo_verificacao}',
                    'no-reply@keychart.com',
                    [email],
                    html_message=email_html,
                    fail_silently=False,
                )
                messages.success(request, 'Usuário criado! Um e-mail com o código de verificação foi enviado.')
        elif request.POST.get('verificar_codigo'):
            codigo = request.POST.get('codigo_verificacao')
            # Busca o último usuário criado inativo
            user = User.objects.filter(is_active=False).order_by('-id').first()
            if not user:
                messages.error(request, 'Nenhum usuário pendente de verificação.')
            else:
                try:
                    cod_obj = CodigoVerificacao.objects.get(user=user)
                    if cod_obj.codigo == codigo:
                        user.is_active = True
                        user.save()
                        cod_obj.delete()
                        messages.success(request, 'Usuário ativado com sucesso!')
                    else:
                        messages.error(request, 'Código de verificação incorreto.')
                except CodigoVerificacao.DoesNotExist:
                    messages.error(request, 'Código de verificação não encontrado.')
        elif request.POST.get('delete_user'):
            user_id = request.POST.get('delete_user')
            User.objects.filter(id=user_id).delete()
            messages.success(request, 'Usuário excluído com sucesso!')
        elif request.POST.get('toggle_user'):
            user_id = request.POST.get('toggle_user')
            user = User.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            messages.success(request, 'Status do usuário alterado!')
        elif request.POST.get('edit_user'):
            user_id = request.POST.get('edit_user')
            user = User.objects.get(id=user_id)
            user.first_name = request.POST.get('nome')
            user.email = request.POST.get('email')
            if request.POST.get('senha'):
                user.set_password(request.POST.get('senha'))
            user.save()
            messages.success(request, 'Usuário editado com sucesso!')
    usuarios = User.objects.all()
    return render(request, 'configuracoes/configuracoes.html', {'usuarios': usuarios})