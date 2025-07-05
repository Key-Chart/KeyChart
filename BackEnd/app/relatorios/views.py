from django.shortcuts import render
from django.db.models import Count, Q, Avg, Sum
from app.competicoes.models import Competicao, Categoria, PartidaKumite, ResultadoKata, ChaveamentoKata, ChaveamentoKumite
from app.atletas.models import Atleta
from datetime import datetime, timedelta
from django.utils import timezone

def relatorio(request):
    # Dados gerais do sistema
    total_competicoes = Competicao.objects.count()
    competicoes_ativas = Competicao.objects.filter(status='Ativa').count()
    competicoes_finalizadas = Competicao.objects.filter(status='Finalizada').count()
    
    # Dados de atletas
    total_atletas = Atleta.objects.count()
    atletas_masculinos = Atleta.objects.filter(sexo='M').count()
    atletas_femininos = Atleta.objects.filter(sexo='F').count()
    
    # Distribuição por estado
    distribuicao_estados = Atleta.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    # Distribuição por faixa
    distribuicao_faixas = Atleta.objects.values('faixa').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Dados de partidas (últimos 30 dias)
    data_limite = timezone.now() - timedelta(days=30)
    partidas_recentes = PartidaKumite.objects.filter(data_criacao__gte=data_limite)
    total_partidas = partidas_recentes.count()
    partidas_finalizadas = partidas_recentes.filter(status='finalizada').count()
    partidas_em_andamento = partidas_recentes.filter(status='em_andamento').count()
    partidas_agendadas = partidas_recentes.filter(status='agendada').count()
    
    # Estatísticas de kata
    total_resultados_kata = ResultadoKata.objects.count()
    media_notas_kata = ResultadoKata.objects.aggregate(
        media=Avg('total')
    )['media'] or 0
    
    # Top 10 atletas por performance em kata
    top_atletas_kata = ResultadoKata.objects.values(
        'atleta__nome_completo', 
        'atleta__academia__nome',
        'atleta__estado'
    ).annotate(
        media_total=Avg('total'),
        participacoes=Count('id')
    ).filter(participacoes__gte=3).order_by('-media_total')[:10]
    
    # Competições mais recentes
    competicoes_recentes = Competicao.objects.select_related().order_by('-data_inicio')[:5]
    
    # Categorias mais populares
    categorias_populares = Categoria.objects.annotate(
        total_atletas=Count('atleta')
    ).order_by('-total_atletas')[:10]
    
    # Dados para gráficos
    # Evolução de inscrições por mês (últimos 6 meses)
    meses_passados = []
    inscricoes_por_mes = []
    
    for i in range(6):
        data_mes = timezone.now() - timedelta(days=30*i)
        inicio_mes = data_mes.replace(day=1)
        if i == 0:
            fim_mes = timezone.now()
        else:
            proximo_mes = inicio_mes.replace(day=28) + timedelta(days=4)
            fim_mes = proximo_mes - timedelta(days=proximo_mes.day)
        
        inscricoes = Atleta.objects.filter(
            data_inscricao__gte=inicio_mes,
            data_inscricao__lte=fim_mes
        ).count()
        
        meses_passados.append(data_mes.strftime('%m/%Y'))
        inscricoes_por_mes.append(inscricoes)
    
    # Reverter para ordem cronológica
    meses_passados.reverse()
    inscricoes_por_mes.reverse()
    
    # Distribuição de idades
    idades_distribuicao = []
    faixas_etarias = [
        ('13-17', 13, 17),
        ('18-25', 18, 25), 
        ('26-35', 26, 35),
        ('36-45', 36, 45),
        ('46+', 46, 100)
    ]
    
    for nome, idade_min, idade_max in faixas_etarias:
        count = Atleta.objects.filter(idade__gte=idade_min, idade__lte=idade_max).count()
        idades_distribuicao.append({'faixa': nome, 'total': count})
    
    # Academias com mais atletas
    top_academias = Atleta.objects.values(
        'academia__nome', 
        'academia__cidade',
        'academia__estado'
    ).annotate(
        total_atletas=Count('id')
    ).filter(academia__nome__isnull=False).order_by('-total_atletas')[:10]
    
    # Performance por modalidade/tipo
    performance_modalidades = Categoria.objects.values('tipo').annotate(
        total_categorias=Count('id'),
        total_atletas=Count('atleta')
    ).order_by('-total_atletas')
    
    context = {
        # Estatísticas gerais
        'total_competicoes': total_competicoes,
        'competicoes_ativas': competicoes_ativas,
        'competicoes_finalizadas': competicoes_finalizadas,
        'total_atletas': total_atletas,
        'atletas_masculinos': atletas_masculinos,
        'atletas_femininos': atletas_femininos,
        
        # Dados de partidas
        'total_partidas': total_partidas,
        'partidas_finalizadas': partidas_finalizadas,
        'partidas_em_andamento': partidas_em_andamento,
        'partidas_agendadas': partidas_agendadas,
        
        # Estatísticas de kata
        'total_resultados_kata': total_resultados_kata,
        'media_notas_kata': round(media_notas_kata, 2),
        
        # Listas e rankings
        'distribuicao_estados': distribuicao_estados,
        'distribuicao_faixas': distribuicao_faixas,
        'top_atletas_kata': top_atletas_kata,
        'competicoes_recentes': competicoes_recentes,
        'categorias_populares': categorias_populares,
        'top_academias': top_academias,
        'performance_modalidades': performance_modalidades,
        'idades_distribuicao': idades_distribuicao,
        
        # Dados para gráficos
        'meses_labels': meses_passados,
        'inscricoes_data': inscricoes_por_mes,
        
        # Calculadas
        'taxa_finalizacao_partidas': round((partidas_finalizadas / total_partidas * 100) if total_partidas > 0 else 0, 1),
        'atletas_por_competicao': round(total_atletas / total_competicoes, 1) if total_competicoes > 0 else 0,
    }
    
    return render(request, 'relatorios/relatorio.html', context)