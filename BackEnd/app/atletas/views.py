from django.shortcuts import render
from django.shortcuts import render
from app.competicoes.models import Competicao, Categoria
from django.http import JsonResponse

# Função para listar todos os atletas
def atletas(request):
    return render(request, 'atletas/equipes_atletas.html')

# Função para renderizar a tela de perfil do atleta
def perfil_atleta(request):
    return render(request, 'atletas/perfil_atleta.html')

# Função para a renderizar a tela de inscrições
def inscricoes_view(request):
    return render(request, 'atletas/inscricoes.html')

# Função para listar todas as competições para a tela de inscrição
def inscricoes_view(request):
    competicoes = Competicao.objects.filter(inscricoes_abertas=True, status='Ativa').order_by('data_inicio')

    # Pré-carrega todas as categorias organizadas por competição
    todas_categorias = {}
    categorias = Categoria.objects.filter(competicao__in=competicoes).select_related('competicao')

    for categoria in categorias:
        competicao_id = categoria.competicao.id
        if competicao_id not in todas_categorias:
            todas_categorias[competicao_id] = []
        todas_categorias[competicao_id].append(categoria)

    context = {
        'competicoes': competicoes,
        'todas_categorias': todas_categorias,
    }
    return render(request, 'atletas/inscricoes.html', context)

# Função para carregar todas as categorias
def carregar_categorias(request, competicao_id):
    try:
        categorias = Categoria.objects.filter(competicao_id=competicao_id).values('id', 'nome', 'tipo', 'sexo')
        return JsonResponse({'categorias': list(categorias)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)