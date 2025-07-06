from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from app.atletas.models import Atleta
from app.competicoes.models import (
    Competicao, Categoria, ResultadoKata, ChaveamentoKata,
    PartidaKumite, PontuacaoKumite, ChaveamentoKumite
)
import json

def portal_atleta(request, atleta_id=None):
    """
    Portal principal do atleta com dados dinâmicos
    """
    # Se não foi passado ID, pega o primeiro atleta (ou pode implementar autenticação)
    if atleta_id is None:
        atleta = Atleta.objects.first()
        if not atleta:
            messages.error(request, 'Nenhum atleta encontrado no sistema.')
            return render(request, 'portal_atleta/portal_atleta.html', {'error': 'no_athlete'})
    else:
        atleta = get_object_or_404(Atleta, id=atleta_id)
    
    # Dados básicos do atleta
    today = timezone.now().date()
    
    # Competições próximas (futuras)
    competicoes_proximas = Competicao.objects.filter(
        atletas=atleta,
        data_inicio__gte=today
    ).order_by('data_inicio')[:5]
    
    # Competições passadas
    competicoes_passadas = Competicao.objects.filter(
        atletas=atleta,
        data_inicio__lt=today
    ).order_by('-data_inicio')[:10]
    
    # Todas as competições do atleta
    todas_competicoes = Competicao.objects.filter(
        atletas=atleta
    ).order_by('-data_inicio')
    
    # Resultados de Kata (todos para estatísticas)
    todos_resultados_kata = ResultadoKata.objects.filter(
        atleta=atleta
    ).select_related('competicao', 'categoria').order_by('-data_criacao')
    
    # Resultados de Kata (limitados para exibição)
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