from django.shortcuts import render
from django.db.models import Q, Count
from app.competicoes.models import PartidaKumite, Competicao, Categoria
from django.core.paginator import Paginator
from datetime import datetime

# Rota para renderizar a pagina de Partidas
def partidas(request):
    # Buscar todas as partidas iniciadas (em andamento ou finalizadas)
    partidas_queryset = PartidaKumite.objects.filter(
        status__in=['em_andamento', 'finalizada']
    ).select_related(
        'atleta1', 'atleta2', 'categoria', 'competicao', 
        'atleta1__academia', 'atleta2__academia'
    ).order_by('-data_inicio', '-data_criacao')
    
    # Filtros de busca
    search_query = request.GET.get('q')
    competicao_id = request.GET.get('competicao')
    data_filtro = request.GET.get('data')
    status_filtro = request.GET.get('status')
    
    if search_query:
        partidas_queryset = partidas_queryset.filter(
            Q(atleta1__nome_completo__icontains=search_query) |
            Q(atleta2__nome_completo__icontains=search_query) |
            Q(competicao__nome__icontains=search_query) |
            Q(categoria__nome__icontains=search_query)
        )
    
    if competicao_id:
        partidas_queryset = partidas_queryset.filter(competicao_id=competicao_id)
    
    if data_filtro:
        try:
            data_obj = datetime.strptime(data_filtro, '%Y-%m-%d').date()
            partidas_queryset = partidas_queryset.filter(data_inicio__date=data_obj)
        except ValueError:
            pass
    
    if status_filtro:
        partidas_queryset = partidas_queryset.filter(status=status_filtro)
    
    # Paginação
    paginator = Paginator(partidas_queryset, 10)
    page_number = request.GET.get('page')
    partidas = paginator.get_page(page_number)
    
    # Estatísticas
    total_partidas = PartidaKumite.objects.count()
    partidas_em_andamento = PartidaKumite.objects.filter(status='em_andamento').count()
    partidas_finalizadas = PartidaKumite.objects.filter(status='finalizada').count()
    partidas_agendadas = PartidaKumite.objects.filter(status='agendada').count()
    
    # Competições para filtro
    competicoes = Competicao.objects.filter(status='Ativa').order_by('nome')
    
    context = {
        'partidas': partidas,
        'competicoes': competicoes,
        'total_partidas': total_partidas,
        'partidas_em_andamento': partidas_em_andamento,
        'partidas_finalizadas': partidas_finalizadas,
        'partidas_agendadas': partidas_agendadas,
        'search_query': search_query,
        'competicao_selecionada': competicao_id,
        'data_filtro': data_filtro,
        'status_filtro': status_filtro,
    }
    
    return render(request, 'partidas_chaveamento/partidas.html', context)

def chaveamento(request):
    return render(request, 'partidas_chaveamento/chaveamento.html')