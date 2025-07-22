from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import InscricaoOnline, LogInscricao
from app.competicoes.models import Competicao, Categoria
from app.atletas.models import Academia, Atleta
import json
import logging

logger = logging.getLogger(__name__)

def inscricao_competicao(request, competicao_id):
    """
    Página principal de inscrição para uma competição específica
    """
    competicao = get_object_or_404(Competicao, id=competicao_id, inscricoes_abertas=True)
    
    # Verificar se as inscrições ainda estão abertas
    if competicao.inscricoes_data_limite and timezone.now().date() > competicao.inscricoes_data_limite:
        messages.warning(request, 'O prazo para inscrições desta competição já expirou.')
        return render(request, 'inscricoes_online/inscricoes_fechadas.html', {'competicao': competicao})
    
    # Buscar categorias disponíveis
    categorias = Categoria.objects.filter(competicao=competicao).order_by('nome')
    
    # Buscar academias para autocomplete
    academias = Academia.objects.filter(competicao=competicao).values(
        'nome', 'cidade', 'estado'
    ).distinct()
    
    context = {
        'competicao': competicao,
        'categorias': categorias,
        'academias': list(academias),
        'estados': [
            {'sigla': 'AC', 'nome': 'Acre'},
            {'sigla': 'AL', 'nome': 'Alagoas'},
            {'sigla': 'AP', 'nome': 'Amapá'},
            {'sigla': 'AM', 'nome': 'Amazonas'},
            {'sigla': 'BA', 'nome': 'Bahia'},
            {'sigla': 'CE', 'nome': 'Ceará'},
            {'sigla': 'DF', 'nome': 'Distrito Federal'},
            {'sigla': 'ES', 'nome': 'Espírito Santo'},
            {'sigla': 'GO', 'nome': 'Goiás'},
            {'sigla': 'MA', 'nome': 'Maranhão'},
            {'sigla': 'MT', 'nome': 'Mato Grosso'},
            {'sigla': 'MS', 'nome': 'Mato Grosso do Sul'},
            {'sigla': 'MG', 'nome': 'Minas Gerais'},
            {'sigla': 'PA', 'nome': 'Pará'},
            {'sigla': 'PB', 'nome': 'Paraíba'},
            {'sigla': 'PR', 'nome': 'Paraná'},
            {'sigla': 'PE', 'nome': 'Pernambuco'},
            {'sigla': 'PI', 'nome': 'Piauí'},
            {'sigla': 'RJ', 'nome': 'Rio de Janeiro'},
            {'sigla': 'RN', 'nome': 'Rio Grande do Norte'},
            {'sigla': 'RS', 'nome': 'Rio Grande do Sul'},
            {'sigla': 'RO', 'nome': 'Rondônia'},
            {'sigla': 'RR', 'nome': 'Roraima'},
            {'sigla': 'SC', 'nome': 'Santa Catarina'},
            {'sigla': 'SP', 'nome': 'São Paulo'},
            {'sigla': 'SE', 'nome': 'Sergipe'},
            {'sigla': 'TO', 'nome': 'Tocantins'},
        ]
    }
    
    return render(request, 'inscricoes_online/inscricao.html', context)

@require_POST
def processar_inscricao(request, competicao_id):
    """
    Processa o formulário de inscrição
    """
    competicao = get_object_or_404(Competicao, id=competicao_id, inscricoes_abertas=True)
    
    try:
        with transaction.atomic():
            # Extrair dados do formulário
            dados = {
                'nome_completo': request.POST.get('nome_completo', '').strip(),
                'data_nascimento': request.POST.get('data_nascimento'),
                'cpf': request.POST.get('cpf', '').strip(),
                'rg': request.POST.get('rg', '').strip(),
                'sexo': request.POST.get('sexo'),
                'email': request.POST.get('email', '').strip().lower(),
                'telefone': request.POST.get('telefone', '').strip(),
                'faixa': request.POST.get('faixa'),
                'peso': request.POST.get('peso'),
                'altura': request.POST.get('altura'),
                'cidade': request.POST.get('cidade', '').strip(),
                'estado': request.POST.get('estado'),
                'academia_nome': request.POST.get('academia_nome', '').strip(),
                'academia_cidade': request.POST.get('academia_cidade', '').strip(),
                'academia_estado': request.POST.get('academia_estado'),
                'categoria_id': request.POST.get('categoria_id'),
                'forma_pagamento': request.POST.get('forma_pagamento'),
            }
            
            # Validações básicas
            campos_obrigatorios = [
                'nome_completo', 'data_nascimento', 'sexo', 'email', 'telefone',
                'faixa', 'peso', 'altura', 'cidade', 'estado', 'academia_nome',
                'academia_cidade', 'academia_estado', 'categoria_id'
            ]
            
            for campo in campos_obrigatorios:
                if not dados[campo]:
                    return JsonResponse({
                        'success': False,
                        'message': f'Campo obrigatório não preenchido: {campo}'
                    })
            
            # Verificar se já existe inscrição com este email
            if InscricaoOnline.objects.filter(competicao=competicao, email=dados['email']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Já existe uma inscrição com este email para esta competição.'
                })
            
            # Buscar categoria
            categoria = get_object_or_404(Categoria, id=dados['categoria_id'], competicao=competicao)
            
            # Buscar ou criar academia
            academia, created = Academia.objects.get_or_create(
                nome=dados['academia_nome'],
                competicao=competicao,
                defaults={
                    'cidade': dados['academia_cidade'],
                    'estado': dados['academia_estado'],
                }
            )
            
            # Criar inscrição
            inscricao = InscricaoOnline.objects.create(
                competicao=competicao,
                categoria=categoria,
                nome_completo=dados['nome_completo'],
                data_nascimento=dados['data_nascimento'],
                cpf=dados['cpf'],
                rg=dados['rg'],
                sexo=dados['sexo'],
                email=dados['email'],
                telefone=dados['telefone'],
                faixa=dados['faixa'],
                peso=dados['peso'],
                altura=dados['altura'],
                cidade=dados['cidade'],
                estado=dados['estado'],
                academia_nome=dados['academia_nome'],
                academia_cidade=dados['academia_cidade'],
                academia_estado=dados['academia_estado'],
                academia=academia,
                forma_pagamento=dados['forma_pagamento'],
                ip_inscricao=get_client_ip(request)
            )
            
            # Upload da foto se fornecida
            if 'foto' in request.FILES:
                inscricao.foto = request.FILES['foto']
                inscricao.save()
            
            # Criar log da inscrição
            LogInscricao.objects.create(
                inscricao=inscricao,
                acao='Inscrição criada',
                descricao=f'Inscrição realizada na competição {competicao.nome}',
                ip=get_client_ip(request)
            )
            
            # Enviar email de confirmação
            enviar_email_confirmacao(inscricao)
            
            # Criar atleta no sistema interno (integração)
            criar_atleta_sistema_interno(inscricao)
            
            return JsonResponse({
                'success': True,
                'message': 'Inscrição realizada com sucesso!',
                'numero_inscricao': inscricao.numero_inscricao,
                'uuid': str(inscricao.uuid)
            })
            
    except Exception as e:
        logger.error(f"Erro ao processar inscrição: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Erro interno do servidor. Tente novamente.'
        })

def status_inscricao(request, uuid):
    """
    Página de status da inscrição
    """
    inscricao = get_object_or_404(InscricaoOnline, uuid=uuid)
    
    context = {
        'inscricao': inscricao,
        'logs': inscricao.logs.all()[:10]  # Últimos 10 logs
    }
    
    return render(request, 'inscricoes_online/status.html', context)

@require_POST
def confirmar_pagamento(request, uuid):
    """
    Simula confirmação de pagamento (para testes)
    Em produção, isso seria feito via webhook do Mercado Pago
    """
    inscricao = get_object_or_404(InscricaoOnline, uuid=uuid)
    
    if inscricao.status == 'pendente':
        inscricao.status = 'pago'
        inscricao.save()
        
        # Criar log
        LogInscricao.objects.create(
            inscricao=inscricao,
            acao='Pagamento confirmado',
            descricao='Pagamento confirmado - simulação para testes',
            ip=get_client_ip(request)
        )
        
        messages.success(request, 'Pagamento confirmado com sucesso!')
    
    return redirect('inscricoes_online:status', uuid=uuid)

def get_client_ip(request):
    """Obtém o IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def enviar_email_confirmacao(inscricao):
    """
    Envia email de confirmação da inscrição com dados de acesso
    """
    try:
        assunto = f'Confirmação de Inscrição - {inscricao.competicao.nome}'
        
        # Renderizar template do email
        contexto = {
            'inscricao': inscricao,
            'competicao': inscricao.competicao,
            'url_status': f"{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000'}/inscricoes/{inscricao.uuid}/status/",
        }
        
        mensagem_html = render_to_string('inscricoes_online/emails/confirmacao.html', contexto)
        mensagem_texto = render_to_string('inscricoes_online/emails/confirmacao.txt', contexto)
        
        # Enviar email
        send_mail(
            subject=assunto,
            message=mensagem_texto,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@keychart.com',
            recipient_list=[inscricao.email],
            html_message=mensagem_html,
            fail_silently=False,
        )
        
        # Marcar senha como enviada
        inscricao.senha_enviada = True
        inscricao.save()
        
        # Log do envio
        LogInscricao.objects.create(
            inscricao=inscricao,
            acao='Email enviado',
            descricao='Email de confirmação enviado com sucesso'
        )
        
    except Exception as e:
        logger.error(f"Erro ao enviar email para {inscricao.email}: {str(e)}")
        
        # Log do erro
        LogInscricao.objects.create(
            inscricao=inscricao,
            acao='Erro no email',
            descricao=f'Falha ao enviar email: {str(e)}'
        )

def criar_atleta_sistema_interno(inscricao):
    """
    Cria o atleta no sistema interno para integração completa
    """
    try:
        # Verificar se já existe
        if Atleta.objects.filter(email=inscricao.email, competicao=inscricao.competicao).exists():
            return
        
        # Criar atleta no sistema interno
        atleta = Atleta.objects.create(
            competicao=inscricao.competicao,
            categoria=inscricao.categoria,
            academia=inscricao.academia,
            nome_completo=inscricao.nome_completo,
            data_nascimento=inscricao.data_nascimento,
            sexo=inscricao.sexo,
            idade=inscricao.get_idade(),
            peso=inscricao.peso,
            altura=inscricao.altura,
            email=inscricao.email,
            telefone=inscricao.telefone,
            faixa=inscricao.faixa,
            cidade=inscricao.cidade,
            estado=inscricao.estado,
            foto=inscricao.foto,
        )
        
        # Log da integração
        LogInscricao.objects.create(
            inscricao=inscricao,
            acao='Atleta criado',
            descricao=f'Atleta integrado ao sistema interno (ID: {atleta.id})'
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar atleta no sistema interno: {str(e)}")
        
        LogInscricao.objects.create(
            inscricao=inscricao,
            acao='Erro na integração',
            descricao=f'Falha ao criar atleta no sistema: {str(e)}'
        )

def listar_categorias_competicao(request, competicao_id):
    """
    API para listar categorias de uma competição (AJAX)
    """
    competicao = get_object_or_404(Competicao, id=competicao_id)
    categorias = Categoria.objects.filter(competicao=competicao).values(
        'id', 'nome', 'sexo', 'tipo'
    )
    
    return JsonResponse({
        'categorias': list(categorias)
    })

# View para listar competições com inscrições abertas (landing page)
def competicoes_abertas(request):
    """
    Lista todas as competições com inscrições abertas
    """
    competicoes = Competicao.objects.filter(
        inscricoes_abertas=True,
        status='Ativa'
    ).order_by('data_inicio')
    
    return render(request, 'inscricoes_online/competicoes_abertas.html', {
        'competicoes': competicoes
    })
