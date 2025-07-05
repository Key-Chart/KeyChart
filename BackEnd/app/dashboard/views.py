from django.shortcuts import render
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from app.autenticacao.decorators import login_required_custom
from app.competicoes.models import Competicao, Academia, PartidaKumite, ResultadoKata
from app.atletas.models import Atleta

# View para a página de dashboard
#@login_required_custom
def dashboard(request):
    # Estatísticas gerais
    total_competicoes = Competicao.objects.count()
    total_academias = Academia.objects.count()
    total_atletas = Atleta.objects.count()
    
    # Partidas de hoje
    hoje = timezone.now().date()
    partidas_hoje = PartidaKumite.objects.filter(
        data_inicio__date=hoje
    ).count()
    
    partidas_em_andamento = PartidaKumite.objects.filter(
        status='em_andamento'
    ).count()
    
    # Competições recentes (últimos 30 dias)
    data_limite = timezone.now() - timedelta(days=30)
    competicoes_recentes = Competicao.objects.filter(
        data_inicio__gte=data_limite.date()
    ).order_by('-data_inicio')[:5]
    
    # Próximas partidas (próximos 7 dias)
    proxima_semana = timezone.now() + timedelta(days=7)
    proximas_partidas = PartidaKumite.objects.filter(
        data_inicio__gte=timezone.now(),
        data_inicio__lte=proxima_semana,
        status__in=['agendada', 'em_andamento']
    ).select_related(
        'atleta1', 'atleta2', 'atleta1__academia', 'atleta2__academia', 'chaveamento__categoria'
    ).order_by('data_inicio')[:10]
    
    # Top academias por número de atletas
    top_academias = Academia.objects.annotate(
        total_atletas=Count('atleta')
    ).filter(total_atletas__gt=0).order_by('-total_atletas')[:10]
    
    # Distribuição por faixas
    distribuicao_faixas = Atleta.objects.values('faixa').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Estatísticas de resultados kata (média de notas)
    media_kata = ResultadoKata.objects.aggregate(
        media_geral=Avg('total')
    )['media_geral'] or 0
    
    # Atletas mais ativos (com mais participações)
    atletas_ativos = Atleta.objects.annotate(
        participacoes=Count('resultados_kata') + Count('partidas_kumite_atleta1') + Count('partidas_kumite_atleta2')
    ).filter(participacoes__gt=0).order_by('-participacoes')[:5]
    
    # Dados para gráficos - Inscrições por mês (últimos 6 meses)
    meses_atras = timezone.now() - timedelta(days=180)
    inscricoes_por_mes = []
    labels_meses = []
    
    for i in range(6):
        mes_atual = timezone.now() - timedelta(days=30*i)
        mes_inicio = mes_atual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mes_fim = (mes_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        total_mes = Atleta.objects.filter(
            data_inscricao__gte=mes_inicio,
            data_inscricao__lte=mes_fim
        ).count()
        
        inscricoes_por_mes.insert(0, total_mes)
        labels_meses.insert(0, mes_atual.strftime('%b/%Y'))
    
    # Distribuição por sexo
    distribuicao_sexo = Atleta.objects.values('sexo').annotate(
        total=Count('id')
    )
    
    masculinos = next((item['total'] for item in distribuicao_sexo if item['sexo'] == 'M'), 0)
    femininos = next((item['total'] for item in distribuicao_sexo if item['sexo'] == 'F'), 0)
    
    # Estados com mais atletas
    distribuicao_estados = Atleta.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    context = {
        # Estatísticas principais
        'total_competicoes': total_competicoes,
        'total_academias': total_academias,
        'total_atletas': total_atletas,
        'partidas_hoje': partidas_hoje,
        'partidas_em_andamento': partidas_em_andamento,
        'media_kata': round(media_kata, 2),
        
        # Listas
        'competicoes_recentes': competicoes_recentes,
        'proximas_partidas': proximas_partidas,
        'top_academias': top_academias,
        'atletas_ativos': atletas_ativos,
        'distribuicao_faixas': distribuicao_faixas,
        'distribuicao_estados': distribuicao_estados,
        
        # Dados para gráficos
        'inscricoes_data': inscricoes_por_mes,
        'labels_meses': labels_meses,
        'masculinos': masculinos,
        'femininos': femininos,
        
        # Dados adicionais
        'data_atual': timezone.now(),
    }
    
    return render(request, 'dashboard/dashboard.html', context)

# View para a sidebar
def sidebar(request):
    return render(request, 'dashboard/sidebar.html')
