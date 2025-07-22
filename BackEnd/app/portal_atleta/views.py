from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Sum, Avg, F
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.conf import settings
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Modelos
from .models import AtletaUser, NotificacaoAtleta, PreferenciaAtleta, LogAtividadeAtleta, SessaoAtleta
from app.inscricoes_online.models import InscricaoOnline, LogInscricao
from app.atletas.models import Atleta
from app.competicoes.models import (
    Competicao, Categoria, ResultadoKata, ChaveamentoKata,
    PartidaKumite, PontuacaoKumite, ChaveamentoKumite
)

def get_client_ip(request):
    """Obtém o IP real do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def criar_log_atividade(atleta, acao, descricao, request, dados_extras=None):
    """Cria log de atividade do atleta"""
    try:
        LogAtividadeAtleta.objects.create(
            atleta=atleta,
            acao=acao,
            descricao=descricao,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            dados_extras=dados_extras
        )
    except Exception as e:
        # Log silencioso para não quebrar a aplicação
        pass

def login_atleta(request):
    """
    View de login para atletas usando credenciais das inscrições online
    """
    # DEBUG: Mostrar emails e senhas cadastrados
    if request.method == 'POST':
        print('=== DEBUG LOGIN ATLETA ===')
        from app.inscricoes_online.models import InscricaoOnline
        for insc in InscricaoOnline.objects.all():
            print(f"Email: {insc.email} | Senha: {insc.senha_atleta}")
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Por favor, preencha email e senha.')
            return render(request, 'portal_atleta/login_atleta.html')
        
        try:
            # Buscar inscrição com as credenciais
            inscricao = InscricaoOnline.objects.get(
                email=email,
                senha_atleta=password
            )
            
            # Criar ou buscar usuário atleta
            atleta_user, created = AtletaUser.objects.get_or_create(
                email=email,
                defaults={
                    'nome_completo': inscricao.nome_completo,
                    'telefone': inscricao.telefone,
                    'inscricao_origem': inscricao,
                }
            )
            
            if created:
                # Criar preferências padrão
                PreferenciaAtleta.objects.create(atleta=atleta_user)
                
                # Notificação de boas-vindas
                NotificacaoAtleta.objects.create(
                    atleta=atleta_user,
                    tipo='sistema',
                    titulo='Bem-vindo ao Portal do Atleta!',
                    mensagem=f'Olá {atleta_user.nome_completo}! Seja bem-vindo ao seu portal personalizado.',
                    prioridade='alta'
                )
            
            # Atualizar último acesso
            atleta_user.ultimo_acesso = timezone.now()
            atleta_user.save()
            
            # Marcar primeiro acesso se necessário
            if atleta_user.primeiro_acesso:
                atleta_user.marcar_primeiro_acesso()
            
            # Criar sessão personalizada
            SessaoAtleta.objects.create(
                atleta=atleta_user,
                session_key=request.session.session_key or request.session.create(),
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Login personalizado (usando session)
            request.session['atleta_id'] = atleta_user.id
            request.session['atleta_email'] = atleta_user.email
            request.session['atleta_nome'] = atleta_user.nome_completo
            
            # Log da atividade
            criar_log_atividade(
                atleta_user, 
                'login', 
                f'Login realizado com sucesso via {get_client_ip(request)}',
                request
            )
            
            messages.success(request, f'Bem-vindo, {atleta_user.nome_completo}!')
            return redirect('portal_atleta:dashboard')
            
        except InscricaoOnline.DoesNotExist:
            messages.error(request, 'Email ou senha inválidos.')
            return render(request, 'portal_atleta/login_atleta.html')
        
        except Exception as e:
            import traceback
            print('=== ERRO INTERNO LOGIN ATLETA ===')
            print(e)
            traceback.print_exc()
            messages.error(request, 'Erro interno. Tente novamente.')
            return render(request, 'portal_atleta/login_atleta.html')
    
    # Se já estiver logado, redireciona
    if request.session.get('atleta_id'):
        return redirect('portal_atleta:dashboard')
    
    return render(request, 'portal_atleta/login_atleta.html')

def logout_atleta(request):
    """Logout do atleta"""
    atleta_id = request.session.get('atleta_id')
    if atleta_id:
        try:
            atleta = AtletaUser.objects.get(id=atleta_id)
            
            # Desativar sessões ativas
            SessaoAtleta.objects.filter(
                atleta=atleta,
                session_key=request.session.session_key
            ).update(ativa=False)
            
            # Log da atividade
            criar_log_atividade(
                atleta, 
                'logout', 
                'Logout realizado',
                request
            )
            
        except AtletaUser.DoesNotExist:
            pass
    
    # Limpar sessão
    request.session.flush()
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('portal_atleta:login')

def atleta_required(view_func):
    """Decorator para exigir login do atleta"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('atleta_id'):
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('portal_atleta:login')
        
        try:
            atleta = AtletaUser.objects.get(id=request.session['atleta_id'])
            if not atleta.is_active:
                messages.error(request, 'Sua conta foi desativada.')
                return redirect('portal_atleta:login')
            
            # Adicionar atleta ao request
            request.atleta = atleta
            return view_func(request, *args, **kwargs)
            
        except AtletaUser.DoesNotExist:
            request.session.flush()
            messages.error(request, 'Sessão inválida. Faça login novamente.')
            return redirect('portal_atleta:login')
    
    return _wrapped_view

@atleta_required
def dashboard(request):
    """
    Dashboard principal do atleta
    """
    atleta = request.atleta
    today = timezone.now().date()
    
    # Inscrições do atleta
    inscricoes = atleta.get_inscricoes().order_by('-data_inscricao')
    
    # Competições
    competicoes_proximas = Competicao.objects.filter(
        inscricoes_online__email=atleta.email,
        data_inicio__gte=today
    ).distinct().order_by('data_inicio')[:5]
    
    competicoes_passadas = Competicao.objects.filter(
        inscricoes_online__email=atleta.email,
        data_inicio__lt=today
    ).distinct().order_by('-data_inicio')[:5]
    
    # Estatísticas gerais
    stats = {
        'total_inscricoes': inscricoes.count(),
        'inscricoes_pagas': inscricoes.filter(status='pago').count(),
        'inscricoes_pendentes': inscricoes.filter(status='pendente').count(),
        'total_competicoes': competicoes_proximas.count() + competicoes_passadas.count(),
        'competicoes_proximas': competicoes_proximas.count(),
    }
    
    # Notificações não lidas
    notificacoes_nao_lidas = atleta.notificacoes.filter(lida=False).order_by('-data_criacao')[:5]
    
    # Atividades recentes
    atividades_recentes = atleta.logs.all().order_by('-data_acao')[:10]
    
    # Gráfico de inscrições por mês (últimos 6 meses)
    seis_meses_atras = today - timedelta(days=180)
    inscricoes_por_mes = defaultdict(int)
    
    # Gerar lista de meses (últimos 6 meses, do mais antigo para o mais recente)
    meses_labels = []
    datas_meses = []
    for i in range(5, -1, -1):
        data = (today.replace(day=1) - timedelta(days=30*i))
        mes_ano = data.strftime('%b/%Y')
        meses_labels.append(mes_ano)
        datas_meses.append(data)

    # Contar inscrições por mês
    inscricoes_por_mes = defaultdict(int)
    for inscricao in inscricoes.filter(data_inscricao__date__gte=seis_meses_atras):
        mes_ano = inscricao.data_inscricao.strftime('%b/%Y')
        inscricoes_por_mes[mes_ano] += 1

    # Preencher meses sem inscrições com 0
    inscricoes_mes_valores = [inscricoes_por_mes.get(mes, 0) for mes in meses_labels]
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Acesso ao dashboard principal',
        request
    )
    
    context = {
        'atleta': atleta,
        'inscricoes_recentes': inscricoes[:5],
        'competicoes_proximas': competicoes_proximas,
        'competicoes_passadas': competicoes_passadas,
        'stats': stats,
        'notificacoes': notificacoes_nao_lidas,
        'atividades': atividades_recentes,
        'inscricoes_por_mes': dict(inscricoes_por_mes),
    }
    
    return render(request, 'portal_atleta/dashboard.html', context)

@atleta_required 
def minhas_inscricoes(request):
    """
    Lista todas as inscrições do atleta
    """
    atleta = request.atleta
    
    # Filtros
    status_filtro = request.GET.get('status', '')
    competicao_filtro = request.GET.get('competicao', '')
    
    # Query base
    inscricoes = atleta.get_inscricoes().select_related('competicao', 'categoria', 'academia')
    
    # Aplicar filtros
    if status_filtro:
        inscricoes = inscricoes.filter(status=status_filtro)
    
    if competicao_filtro:
        inscricoes = inscricoes.filter(competicao__id=competicao_filtro)
    
    # Ordenação
    inscricoes = inscricoes.order_by('-data_inscricao')
    
    # Paginação
    paginator = Paginator(inscricoes, 10)
    page_number = request.GET.get('page')
    inscricoes_paginadas = paginator.get_page(page_number)
    
    # Competições para filtro
    competicoes_disponiveis = Competicao.objects.filter(
        inscricoes_online__email=atleta.email
    ).distinct().order_by('nome')
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Visualização da lista de inscrições',
        request,
        {'filtros': {'status': status_filtro, 'competicao': competicao_filtro}}
    )
    
    context = {
        'atleta': atleta,
        'inscricoes': inscricoes_paginadas,
        'competicoes_disponiveis': competicoes_disponiveis,
        'status_atual': status_filtro,
        'competicao_atual': competicao_filtro,
        'status_choices': InscricaoOnline.STATUS_CHOICES,
    }
    
    return render(request, 'portal_atleta/minhas_inscricoes.html', context)

@atleta_required
def detalhes_inscricao(request, uuid_inscricao):
    """
    Detalhes de uma inscrição específica
    """
    atleta = request.atleta
    
    try:
        inscricao = InscricaoOnline.objects.select_related(
            'competicao', 'categoria', 'academia'
        ).get(uuid=uuid_inscricao, email=atleta.email)
    except InscricaoOnline.DoesNotExist:
        messages.error(request, 'Inscrição não encontrada.')
        return redirect('portal_atleta:minhas_inscricoes')
    
    # Logs da inscrição
    logs_inscricao = LogInscricao.objects.filter(
        inscricao=inscricao
    ).order_by('-data')[:20]
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        f'Visualização de detalhes da inscrição {inscricao.numero_inscricao}',
        request,
        {'inscricao_uuid': str(uuid_inscricao)}
    )
    
    context = {
        'atleta': atleta,
        'inscricao': inscricao,
        'logs': logs_inscricao,
    }
    
    return render(request, 'portal_atleta/detalhes_inscricao.html', context)

@atleta_required
def minhas_competicoes(request):
    """
    Lista todas as competições do atleta
    """
    atleta = request.atleta
    today = timezone.now().date()
    
    # Separar competições
    competicoes_futuras = Competicao.objects.filter(
        inscricoes_online__email=atleta.email,
        data_inicio__gte=today
    ).distinct().order_by('data_inicio')
    
    competicoes_passadas = Competicao.objects.filter(
        inscricoes_online__email=atleta.email,
        data_inicio__lt=today
    ).distinct().order_by('-data_inicio')
    
    # Paginação para competições passadas
    paginator = Paginator(competicoes_passadas, 5)
    page_number = request.GET.get('page')
    competicoes_passadas_paginadas = paginator.get_page(page_number)
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Visualização da lista de competições',
        request
    )
    
    context = {
        'atleta': atleta,
        'competicoes_futuras': competicoes_futuras,
        'competicoes_passadas': competicoes_passadas_paginadas,
    }
    
    return render(request, 'portal_atleta/minhas_competicoes.html', context)

@atleta_required
def detalhes_competicao(request, competicao_id):
    """
    Detalhes de uma competição específica
    """
    atleta = request.atleta
    
    # Verificar se o atleta tem inscrição nesta competição
    try:
        inscricao = InscricaoOnline.objects.get(
            competicao_id=competicao_id,
            email=atleta.email
        )
        competicao = inscricao.competicao
    except InscricaoOnline.DoesNotExist:
        messages.error(request, 'Você não tem inscrição nesta competição.')
        return redirect('portal_atleta:minhas_competicoes')
    
    # Buscar resultados se existirem
    # TODO: Integrar com sistema de resultados quando implementado
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        f'Visualização de detalhes da competição {competicao.nome}',
        request,
        {'competicao_id': competicao_id}
    )
    
    context = {
        'atleta': atleta,
        'competicao': competicao,
        'inscricao': inscricao,
    }
    
    return render(request, 'portal_atleta/detalhes_competicao.html', context)

@atleta_required
def notificacoes(request):
    """
    Central de notificações do atleta
    """
    atleta = request.atleta
    
    # Marcar como lidas se solicitado
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'marcar_todas_lidas':
            atleta.notificacoes.filter(lida=False).update(
                lida=True,
                data_leitura=timezone.now()
            )
            messages.success(request, 'Todas as notificações foram marcadas como lidas.')
            return redirect('portal_atleta:notificacoes')
    
    # Filtros
    tipo_filtro = request.GET.get('tipo', '')
    lida_filtro = request.GET.get('lida', '')
    
    # Query base
    notificacoes_query = atleta.notificacoes.all()
    
    # Aplicar filtros
    if tipo_filtro:
        notificacoes_query = notificacoes_query.filter(tipo=tipo_filtro)
    
    if lida_filtro:
        is_lida = lida_filtro == 'true'
        notificacoes_query = notificacoes_query.filter(lida=is_lida)
    
    # Ordenação
    notificacoes_query = notificacoes_query.order_by('-data_criacao')
    
    # Paginação
    paginator = Paginator(notificacoes_query, 15)
    page_number = request.GET.get('page')
    notificacoes_paginadas = paginator.get_page(page_number)
    
    # Estatísticas
    total_notificacoes = atleta.notificacoes.count()
    nao_lidas = atleta.notificacoes.filter(lida=False).count()
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Acesso à central de notificações',
        request
    )
    
    context = {
        'atleta': atleta,
        'notificacoes': notificacoes_paginadas,
        'total_notificacoes': total_notificacoes,
        'nao_lidas': nao_lidas,
        'tipo_atual': tipo_filtro,
        'lida_atual': lida_filtro,
        'tipos_choices': NotificacaoAtleta.TIPO_CHOICES,
    }
    
    return render(request, 'portal_atleta/notificacoes.html', context)

@atleta_required
@require_POST
def marcar_notificacao_lida(request):
    """
    Marca uma notificação como lida via AJAX
    """
    try:
        notificacao_id = request.POST.get('notificacao_id')
        notificacao = get_object_or_404(
            NotificacaoAtleta, 
            id=notificacao_id, 
            atleta=request.atleta
        )
        
        notificacao.marcar_como_lida()
        
        return JsonResponse({
            'success': True,
            'message': 'Notificação marcada como lida'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro ao marcar notificação como lida'
        }, status=400)

@atleta_required
def configuracoes(request):
    """
    Página de configurações do atleta
    """
    atleta = request.atleta
    
    # Buscar ou criar preferências
    preferencias, created = PreferenciaAtleta.objects.get_or_create(
        atleta=atleta
    )
    
    if request.method == 'POST':
        # Atualizar preferências
        preferencias.receber_email_inscricao = request.POST.get('receber_email_inscricao') == 'on'
        preferencias.receber_email_pagamento = request.POST.get('receber_email_pagamento') == 'on'
        preferencias.receber_email_competicao = request.POST.get('receber_email_competicao') == 'on'
        preferencias.receber_email_resultado = request.POST.get('receber_email_resultado') == 'on'
        
        preferencias.perfil_publico = request.POST.get('perfil_publico') == 'on'
        preferencias.mostrar_resultados = request.POST.get('mostrar_resultados') == 'on'
        preferencias.mostrar_estatisticas = request.POST.get('mostrar_estatisticas') == 'on'
        
        preferencias.tema_escuro = request.POST.get('tema_escuro') == 'on'
        
        preferencias.save()
        
        # Log da alteração
        criar_log_atividade(
            atleta, 
            'alteracao', 
            'Configurações atualizadas',
            request,
            {'preferencias_alteradas': True}
        )
        
        messages.success(request, 'Configurações atualizadas com sucesso!')
        return redirect('portal_atleta:configuracoes')
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Acesso às configurações',
        request
    )
    
    context = {
        'atleta': atleta,
        'preferencias': preferencias,
    }
    
    return render(request, 'portal_atleta/configuracoes.html', context)

@atleta_required
def estatisticas(request):
    """
    Página de estatísticas detalhadas do atleta
    """
    atleta = request.atleta
    today = timezone.now().date()
    
    # Inscrições do atleta
    inscricoes = atleta.get_inscricoes()
    
    # Estatísticas principais
    stats = {
        'total_inscricoes': inscricoes.count(),
        'inscricoes_pagas': inscricoes.filter(status='pago').count(),
        'inscricoes_pendentes': inscricoes.filter(status='pendente').count(),
        'inscricoes_canceladas': inscricoes.filter(status='cancelado').count(),
        'inscricoes_confirmadas': inscricoes.filter(status='confirmado').count(),
        'competicoes_participadas': inscricoes.filter(competicao__data_inicio__lt=today).count(),
        'total_investido': inscricoes.filter(status__in=['pago', 'confirmado']).aggregate(
            total=Sum('valor_inscricao'))['total'] or 0,
    }
    
    # Calcular taxa de participação
    if stats['total_inscricoes'] > 0:
        stats['taxa_participacao'] = round(
            (stats['competicoes_participadas'] / stats['total_inscricoes']) * 100, 1
        )
    else:
        stats['taxa_participacao'] = 0
    
    # Inscrições por mês (últimos 6 meses)
    seis_meses_atras = today - timedelta(days=180)
    inscricoes_por_mes = defaultdict(int)
    meses_labels = []
    
    # Gerar lista de meses (últimos 6 meses, do mais antigo para o mais recente)
    for i in range(5, -1, -1):
        data = (today.replace(day=1) - timedelta(days=30*i))
        mes_ano = data.strftime('%b/%Y')
        meses_labels.append(mes_ano)

    for inscricao in inscricoes.filter(data_inscricao__date__gte=seis_meses_atras):
        mes_ano = inscricao.data_inscricao.strftime('%b/%Y')
        inscricoes_por_mes[mes_ano] += 1
    
    # Preencher meses sem inscrições com 0
    inscricoes_mes_valores = [inscricoes_por_mes.get(mes, 0) for mes in meses_labels]
    
    # Categorias mais participadas
    categorias_stats = []
    categorias_count = inscricoes.values('categoria__nome').annotate(
        count=Count('categoria__nome')
    ).order_by('-count')[:5]
    
    total_categorias = sum(item['count'] for item in categorias_count)
    for item in categorias_count:
        if item['categoria__nome'] and total_categorias > 0:
            categorias_stats.append({
                'nome': item['categoria__nome'],
                'count': item['count'],
                'percentage': round((item['count'] / total_categorias) * 100, 1)
            })
    
    # Modalidades preferidas (baseado nos nomes das categorias)
    modalidades_stats = []
    modalidades_count = {}
    
    for inscricao in inscricoes.select_related('categoria'):
        if inscricao.categoria and inscricao.categoria.nome:
            # Extrair modalidade do nome da categoria (kata, kumite, etc.)
            nome_categoria = inscricao.categoria.nome.lower()
            if 'kata' in nome_categoria:
                modalidade = 'Kata'
            elif 'kumite' in nome_categoria:
                modalidade = 'Kumitê'
            elif 'kata' in nome_categoria and 'equipe' in nome_categoria:
                modalidade = 'Kata em Equipe'
            else:
                modalidade = 'Outras Modalidades'
            
            modalidades_count[modalidade] = modalidades_count.get(modalidade, 0) + 1
    
    total_modalidades = sum(modalidades_count.values())
    for modalidade, count in sorted(modalidades_count.items(), key=lambda x: x[1], reverse=True):
        if total_modalidades > 0:
            modalidades_stats.append({
                'nome': modalidade,
                'count': count,
                'percentage': round((count / total_modalidades) * 100, 1)
            })
    
    # Atividades recentes
    atividades_recentes = atleta.logs.all().order_by('-data_acao')[:10]
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Acesso às estatísticas detalhadas',
        request
    )
    
    context = {
        'atleta': atleta,
        'stats': stats,
        'categorias_stats': categorias_stats,
        'modalidades_stats': modalidades_stats,
        'meses_labels': json.dumps(meses_labels),
        'inscricoes_por_mes': json.dumps(inscricoes_mes_valores),
        'atividades_recentes': atividades_recentes,
    }
    
    return render(request, 'portal_atleta/estatisticas.html', context)

@atleta_required
def perfil(request):
    """
    Perfil completo do atleta com estatísticas e informações pessoais
    """
    atleta = request.atleta
    today = timezone.now().date()
    
    # Dados da inscrição mais recente para preencher informações faltantes
    inscricao_recente = atleta.get_inscricoes().order_by('-data_inscricao').first()
    
    # Preencher dados do atleta com informações da inscrição se necessário
    if inscricao_recente and not atleta.telefone:
        atleta.telefone = inscricao_recente.telefone

    # Preencher dados de endereço dinamicamente (não salva no banco)
    atleta.endereco = getattr(inscricao_recente, 'endereco', '') if inscricao_recente else ''
    atleta.cidade = getattr(inscricao_recente, 'cidade', '') if inscricao_recente else ''
    atleta.estado = getattr(inscricao_recente, 'estado', '') if inscricao_recente else ''
    atleta.cep = getattr(inscricao_recente, 'cep', '') if inscricao_recente else ''
    
    # Estatísticas para o perfil
    inscricoes = atleta.get_inscricoes()
    stats = {
        'total_inscricoes': inscricoes.count(),
        'competicoes_participadas': inscricoes.filter(
            competicao__data_inicio__lt=today
        ).count(),
        'modalidades_praticadas': inscricoes.values('categoria__nome').distinct().count(),
        'total_investido': inscricoes.filter(
            status__in=['pago', 'confirmado']
        ).aggregate(total=Sum('valor_inscricao'))['total'] or 0,
    }
    
    # Conquistas (placeholder - pode ser expandido)
    conquistas = []
    if stats['total_inscricoes'] >= 1:
        conquistas.append({'nome': 'Primeira Inscrição'})
    if stats['total_inscricoes'] >= 5:
        conquistas.append({'nome': 'Atleta Ativo'})
    if stats['total_inscricoes'] >= 10:
        conquistas.append({'nome': 'Veterano'})
    if stats['competicoes_participadas'] >= 5:
        conquistas.append({'nome': 'Competidor Experiente'})
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Visualização do perfil completo',
        request
    )
    
    context = {
        'atleta': atleta,
        'inscricao_recente': inscricao_recente,
        'stats': stats,
        'conquistas': conquistas,
    }
    
    return render(request, 'portal_atleta/perfil.html', context)
    resultados_kata = todos_resultados_kata[:10]
    
    # Resultados de Kumitê (todos para estatísticas)
    todas_partidas_kumite = PartidaKumite.objects.filter(
        Q(atleta1=atleta) | Q(atleta2=atleta),
        status='finalizada'
    ).select_related('competicao', 'categoria', 'vencedor').order_by('-data_criacao')
    
    # Partidas de Kumitê (limitadas para exibição)
    partidas_kumite = todas_partidas_kumite[:10]
    
    # Estatísticas gerais
    total_competicoes = todas_competicoes.count()
    total_kata_resultados = todos_resultados_kata.count()
    total_kumite_partidas = todas_partidas_kumite.count()
    
    # Medalhas/Posições (baseado nos resultados de kata)
    ouro = todos_resultados_kata.filter(posicao=1).count()
    prata = todos_resultados_kata.filter(posicao=2).count()
    bronze = todos_resultados_kata.filter(posicao=3).count()
    
    # Vitórias em kumitê
    vitorias_kumite = todas_partidas_kumite.filter(vencedor=atleta).count()
    derrotas_kumite = todas_partidas_kumite.exclude(vencedor=atleta).exclude(vencedor__isnull=True).count()
    empates_kumite = todas_partidas_kumite.filter(vencedor__isnull=True).count()
    
    # Últimas conquistas (top 3 posições)
    ultimas_conquistas = todos_resultados_kata.filter(
        posicao__lte=3
    ).order_by('-data_criacao')[:5]
    
    # Próximos eventos (competições futuras + treinos fictícios)
    proximos_eventos = []
    for comp in competicoes_proximas:
        proximos_eventos.append({
            'data': comp.data_inicio,
            'evento': comp.nome,
            'tipo': 'Competição',
            'local': comp.local,
            'status': 'Confirmado' if comp.status == 'Ativa' else comp.status
        })
    
    # Dados para gráfico de desempenho (últimos 6 meses)
    seis_meses_atras = today - timedelta(days=180)
    resultados_recentes = todos_resultados_kata.filter(
        data_criacao__gte=seis_meses_atras
    ).order_by('data_criacao')
    
    # Preparar dados do gráfico
    dados_grafico = []
    labels_grafico = []
    for resultado in resultados_recentes:
        dados_grafico.append(float(resultado.total))
        labels_grafico.append(resultado.competicao.nome[:15] + '...' if len(resultado.competicao.nome) > 15 else resultado.competicao.nome)
    
    # Notificações fictícias (podem ser implementadas como modelo próprio depois)
    notificacoes = [
        {
            'titulo': 'Nova competição disponível',
            'mensagem': f'Inscrições abertas para próximas competições.',
            'tempo': '15 min atrás',
            'tipo': 'info'
        },
        {
            'titulo': 'Resultado atualizado',
            'mensagem': 'Seu último resultado foi registrado no sistema.',
            'tempo': '2 horas atrás',
            'tipo': 'success'
        },
        {
            'titulo': 'Lembrete de treino',
            'mensagem': 'Não esqueça do treino de amanhã.',
            'tempo': '1 dia atrás',
            'tipo': 'warning'
        }
    ]
    
    context = {
        'atleta': atleta,
        'competicoes_proximas': competicoes_proximas,
        'competicoes_passadas': competicoes_passadas,
        'todas_competicoes': todas_competicoes,
        'resultados_kata': resultados_kata,
        'partidas_kumite': partidas_kumite,
        'proximos_eventos': proximos_eventos,
        'notificacoes': notificacoes,
        'ultimas_conquistas': ultimas_conquistas,
        # Estatísticas
        'total_competicoes': total_competicoes,
        'total_resultados': total_kata_resultados,
        'total_kumite_partidas': total_kumite_partidas,
        'medalhas': {
            'ouro': ouro,
            'prata': prata,
            'bronze': bronze
        },
        'kumite_stats': {
            'vitorias': vitorias_kumite,
            'derrotas': derrotas_kumite,
            'empates': empates_kumite,
            'total': total_kumite_partidas
        },
        # Dados para JavaScript
        'dados_grafico_json': json.dumps(dados_grafico),
        'labels_grafico_json': json.dumps(labels_grafico),
        'hoje': today,
    }
    
    return render(request, 'portal_atleta/portal_atleta.html', context)

def detalhes_competicao(request, competicao_id):
    """
    Detalhes de uma competição específica
    """
    competicao = get_object_or_404(Competicao, id=competicao_id)
    
    # Verificar se o atleta está inscrito (se houver autenticação implementada)
    # atleta = get_object_or_404(Atleta, user=request.user)  # Para quando implementar auth
    
    context = {
        'competicao': competicao,
        'categorias': competicao.categorias.all(),
        'total_atletas': competicao.atletas.count(),
    }
    
    return render(request, 'portal_atleta/detalhes_competicao.html', context)

def meus_resultados(request, atleta_id=None):
    """
    Página dedicada aos resultados do atleta
    """
    if atleta_id is None:
        atleta = Atleta.objects.first()
    else:
        atleta = get_object_or_404(Atleta, id=atleta_id)
    
    # Filtros
    competicao_filtro = request.GET.get('competicao')
    
    resultados = ResultadoKata.objects.filter(atleta=atleta)
    
    if competicao_filtro:
        resultados = resultados.filter(competicao_id=competicao_filtro)
    
    resultados = resultados.select_related('competicao', 'categoria').order_by('-data_criacao')
    
    # Lista de competições para o filtro
    competicoes_filtro = Competicao.objects.filter(
        atletas=atleta
    ).distinct().order_by('nome')
    
    context = {
        'atleta': atleta,
        'resultados': resultados,
        'competicoes_filtro': competicoes_filtro,
        'competicao_selecionada': competicao_filtro,
    }
    
    return render(request, 'portal_atleta/meus_resultados.html', context)

@atleta_required
def competicoes(request):
    """
    Lista todas as competições disponíveis para inscrição
    """
    atleta = request.atleta
    today = timezone.now().date()
    
    # Filtros
    busca = request.GET.get('busca', '')
    status_filtro = request.GET.get('status', '')
    estado_filtro = request.GET.get('estado', '')
    periodo_filtro = request.GET.get('periodo', '')
    
    # Query base
    competicoes_query = Competicao.objects.all()
    
    # Aplicar filtros
    if busca:
        competicoes_query = competicoes_query.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(local__icontains=busca)
        )
    
    if status_filtro:
        competicoes_query = competicoes_query.filter(status=status_filtro)
    
    if estado_filtro:
        competicoes_query = competicoes_query.filter(local__icontains=estado_filtro)
    
    if periodo_filtro:
        if periodo_filtro == 'este_mes':
            inicio_mes = today.replace(day=1)
            fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            competicoes_query = competicoes_query.filter(
                data_inicio__gte=inicio_mes,
                data_inicio__lte=fim_mes
            )
        elif periodo_filtro == 'proximo_mes':
            proximo_mes = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
            fim_proximo_mes = (proximo_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            competicoes_query = competicoes_query.filter(
                data_inicio__gte=proximo_mes,
                data_inicio__lte=fim_proximo_mes
            )
        elif periodo_filtro == 'proximos_3_meses':
            fim_periodo = today + timedelta(days=90)
            competicoes_query = competicoes_query.filter(
                data_inicio__gte=today,
                data_inicio__lte=fim_periodo
            )
    
    # Ordenação
    competicoes_query = competicoes_query.order_by('data_inicio')
    
    # Paginação
    paginator = Paginator(competicoes_query, 12)
    page_number = request.GET.get('page')
    competicoes = paginator.get_page(page_number)
    
    # Competições disponíveis para inscrição
    competicoes_disponiveis = Competicao.objects.filter(
        status='ativa',
        inscricoes_data_limite__gte=today
    ).order_by('data_inicio')[:20]
    
    # Minhas inscrições
    minhas_inscricoes = atleta.get_inscricoes().select_related('competicao', 'categoria')
    minhas_inscricoes_ids = list(minhas_inscricoes.values_list('competicao_id', flat=True))
    
    # Estados disponíveis para filtro
    estados = Competicao.objects.values_list('local', flat=True).distinct()
    estados_unicos = set()
    for local in estados:
        if local and ',' in local:
            estado = local.split(',')[-1].strip()
            if len(estado) <= 3 and estado.isupper():
                estados_unicos.add(estado)
    estados = sorted(list(estados_unicos))
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        'Navegação na lista de competições',
        request,
        {'filtros': {
            'busca': busca,
            'status': status_filtro,
            'estado': estado_filtro,
            'periodo': periodo_filtro
        }}
    )
    
    context = {
        'atleta': atleta,
        'competicoes': competicoes,
        'competicoes_disponiveis': competicoes_disponiveis,
        'minhas_inscricoes': minhas_inscricoes,
        'minhas_inscricoes_ids': minhas_inscricoes_ids,
        'estados': estados,
        'today': today,
        'total_competicoes': competicoes_query.count(),
        # Filtros atuais
        'filtros': {
            'busca': busca,
            'status': status_filtro,
            'estado': estado_filtro,
            'periodo': periodo_filtro,
        }
    }
    
    return render(request, 'portal_atleta/competicoes.html', context)

@atleta_required
def competicao_detalhes(request, competicao_id):
    """
    Detalhes completos de uma competição específica
    """
    atleta = request.atleta
    today = timezone.now().date()
    
    competicao = get_object_or_404(Competicao, id=competicao_id)
    
    # Verificar se o atleta já está inscrito
    minha_inscricao = atleta.get_inscricoes().filter(competicao=competicao).first()
    ja_inscrito = minha_inscricao is not None
    
    # Categorias da competição
    categorias = competicao.categorias.all().order_by('nome')
    
    # Total de inscritos
    inscricoes_count = InscricaoOnline.objects.filter(competicao=competicao).count()
    
    # Timeline/cronograma (se houver)
    timeline = []
    if competicao.inscricoes_data_limite:
        timeline.append({
            'data': competicao.inscricoes_data_limite,
            'evento': 'Fim das Inscrições',
            'descricao': 'Última data para realizar inscrições',
            'horario': '23:59'
        })
    
    if competicao.data_inicio:
        timeline.append({
            'data': competicao.data_inicio,
            'evento': 'Início da Competição',
            'descricao': 'Cerimônia de abertura e primeiras modalidades',
            'horario': '08:00'
        })
        
        if competicao.data_fim and competicao.data_fim != competicao.data_inicio:
            timeline.append({
                'data': competicao.data_fim,
                'evento': 'Encerramento',
                'descricao': 'Cerimônia de premiação e encerramento',
                'horario': '18:00'
            })
    
    # Ordenar timeline por data
    timeline.sort(key=lambda x: x['data'])
    
    # Log da visualização
    criar_log_atividade(
        atleta, 
        'visualizacao', 
        f'Visualização dos detalhes da competição: {competicao.nome}',
        request,
        {'competicao_id': competicao.id, 'ja_inscrito': ja_inscrito}
    )
    
    context = {
        'atleta': atleta,
        'competicao': competicao,
        'categorias': categorias,
        'inscricoes_count': inscricoes_count,
        'ja_inscrito': ja_inscrito,
        'minha_inscricao': minha_inscricao,
        'timeline': timeline,
        'today': today,
    }
    
    return render(request, 'portal_atleta/competicao_detalhes.html', context)

@atleta_required
@require_POST
def favoritar_competicao(request, competicao_id):
    """
    Adiciona/remove competição dos favoritos do atleta
    """
    atleta = request.atleta
    competicao = get_object_or_404(Competicao, id=competicao_id)
    
    try:
        # Implementar sistema de favoritos se necessário
        # Por enquanto, apenas um retorno de sucesso
        favorited = True  # Simular toggle de favorito
        
        # Log da ação
        criar_log_atividade(
            atleta, 
            'interacao', 
            f'Competição {"favoritada" if favorited else "desfavoritada"}: {competicao.nome}',
            request,
            {'competicao_id': competicao.id, 'acao': 'favoritar' if favorited else 'desfavoritar'}
        )
        
        return JsonResponse({
            'success': True,
            'favorited': favorited,
            'message': f'Competição {"adicionada aos" if favorited else "removida dos"} favoritos!'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro ao processar solicitação.'
        }, status=500)

@atleta_required
def atualizar_perfil(request):
    """
    Atualiza informações pessoais do atleta
    """
    if request.method != 'POST':
        return redirect('portal_atleta:perfil')
    
    atleta = request.atleta
    
    try:
        # Atualizar dados pessoais
        atleta.nome_completo = request.POST.get('nome_completo', atleta.nome_completo)
        atleta.telefone = request.POST.get('telefone', atleta.telefone)
        atleta.cpf = request.POST.get('cpf', atleta.cpf)
        
        # Data de nascimento
        data_nascimento = request.POST.get('data_nascimento')
        if data_nascimento:
            try:
                atleta.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Sexo
        sexo = request.POST.get('sexo')
        if sexo in ['M', 'F']:
            atleta.sexo = sexo
        
        atleta.save()
        
        # Log da atualização
        criar_log_atividade(
            atleta, 
            'atualizacao', 
            'Dados pessoais atualizados',
            request,
            {'campos_atualizados': list(request.POST.keys())}
        )
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        
    except Exception as e:
        messages.error(request, 'Erro ao atualizar perfil. Tente novamente.')
    
    return redirect('portal_atleta:perfil')

@atleta_required  
def atualizar_endereco(request):
    """
    Atualiza informações de endereço do atleta
    """
    if request.method != 'POST':
        return redirect('portal_atleta:perfil')
    
    atleta = request.atleta
    
    try:
        # Atualizar endereço
        atleta.endereco = request.POST.get('endereco', atleta.endereco)
        atleta.cidade = request.POST.get('cidade', atleta.cidade)
        atleta.estado = request.POST.get('estado', atleta.estado)
        atleta.cep = request.POST.get('cep', atleta.cep)
        
        atleta.save()
        
        # Log da atualização
        criar_log_atividade(
            atleta, 
            'atualizacao', 
            'Endereço atualizado',
            request,
            {'endereco_atualizado': True}
        )
        
        messages.success(request, 'Endereço atualizado com sucesso!')
        
    except Exception as e:
        messages.error(request, 'Erro ao atualizar endereço. Tente novamente.')
    
    return redirect('portal_atleta:perfil')

@atleta_required
def excluir_conta(request):
    """
    Exclusão de conta do atleta (com confirmação)
    """
    if request.method == 'POST':
        atleta = request.atleta
        
        try:
            # Log da exclusão antes de deletar
            criar_log_atividade(
                atleta, 
                'exclusao', 
                'Conta excluída pelo próprio usuário',
                request
            )
            
            # Marcar como inativo ao invés de deletar
            atleta.ativo = False
            atleta.data_exclusao = timezone.now()
            atleta.save()
            
            # Logout
            logout(request)
            
            messages.success(request, 'Sua conta foi excluída com sucesso.')
            return redirect('portal_atleta:login')
            
        except Exception as e:
            messages.error(request, 'Erro ao excluir conta. Tente novamente.')
            return redirect('portal_atleta:perfil')
    
    return redirect('portal_atleta:perfil')