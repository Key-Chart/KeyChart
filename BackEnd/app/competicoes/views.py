from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Competicao
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

def criar_competicao(request):
    if request.method == 'POST':
        nome_competicao = request.POST.get('nome')
        modalidade = request.POST.get('modalidade')
        data_inicio = request.POST.get('data_inicio')
        horario = request.POST.get('horario')
        local = request.POST.get('local')
        arbitros = request.POST.get('arbitros')
        regras_especificas = request.POST.get('regras_especificas')
        status = request.POST.get('status')

        if not nome_competicao or not modalidade or not data_inicio or not horario or not local:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('competicoes:home')

        if len(nome_competicao) < 3:
            messages.error(request, 'Nome da competição muito curto.')
            return redirect('competicoes:home')  # Ajusta para sua URL de criação

        nova_competicao = Competicao(
            nome=nome_competicao,
            modalidade=modalidade,
            data_inicio=data_inicio,
            horario=horario,
            local=local,
            arbitros=arbitros,
            regras_especificas=regras_especificas,
            status=status
        )
        nova_competicao.save()
        messages.success(request, 'Competição criada com sucesso!')
        return redirect('competicoes:home')

    # Caso não seja POST, redirecione ou mostre um erro
    return redirect('competicoes:home')

def editar_competicao(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        modalidade = request.POST.get('modalidade')
        data_inicio = request.POST.get('data_inicio')
        horario = request.POST.get('horario')
        local = request.POST.get('local')
        arbitros = request.POST.get('arbitros')
        regras_especificas = request.POST.get('regras_especificas')
        status = request.POST.get('status')

        # Validações
        if not nome or not modalidade or not data_inicio or not horario or not local:
            messages.error(request, 'Preencha todos os campos obrigatórios.')

            return redirect('competicoes:home')

        if len(nome) < 3:
            messages.error(request, 'Nome da competição muito curto.')
            return redirect('competicoes:home')

        # Atualizar os dados da competição
        competicao.nome = nome
        competicao.modalidade = modalidade
        competicao.data_inicio = data_inicio
        competicao.horario = horario
        competicao.local = local
        competicao.arbitros = arbitros
        competicao.regras_especificas = regras_especificas
        competicao.status = status

        # Salvar a competição
        competicao.save()

        messages.success(request, 'Competição atualizada com sucesso!')
        return redirect('competicoes:home')

    # Se não for POST, redireciona para home
    return redirect('competicoes:home')

def excluir_competicao(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)

    if request.method == 'POST':
        try:
            nome_competicao = competicao.nome
            competicao.delete()
            messages.success(request, f'Competição "{nome_competicao}" excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao excluir a competição: {str(e)}')

        return redirect('competicoes:home')

    # Se não for POST, redireciona para home
    return redirect('competicoes:home')


def listar_competicoes(request):
    competicoes = Competicao.objects.all().order_by('-data_inicio')
    # Filtro de busca (campo de texto livre)
    search_query = request.GET.get('q')
    if search_query:
        competicoes = competicoes.filter(
            Q(nome__icontains=search_query) |
            Q(local__icontains=search_query) |
            Q(modalidade__icontains=search_query) |
            Q(arbitros__icontains=search_query)
        )
    # Filtro por status
    if 'status' in request.GET and request.GET['status']:
        competicoes = competicoes.filter(status=request.GET['status'])
    # Filtro por data
    date_filter = request.GET.get('data')
    if date_filter:
        try:
            # Converter a string da data para objeto date
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            # Filtrar por data_inicio
            competicoes = competicoes.filter(data_inicio__date=date_obj)
        except (ValueError, TypeError):
            pass
    context = {
        'listar_competicoes': competicoes,
        'status_choices': ['Ativa', 'Finalizada', 'Em breve'],
    }
    return render(request, 'competicoes/competicoes.html', context)

def competicoes(request):
    listar_competicoes = Competicao.objects.all()
    total_competicoes = Competicao.objects.all().count()
    competicoes_ativas = Competicao.objects.filter(status='Ativa').count()
    competicoes_finalizadas = Competicao.objects.filter(status='Finalizada').count()

    contex = {
        'total_competicoes': total_competicoes,
        'competicoes_ativas': competicoes_ativas,
        'competicoes_finalizadas': competicoes_finalizadas,
        'listar_competicoes': listar_competicoes
    }
    return render(request, 'competicoes/competicoes.html', contex)

def categoria(request):
    return render(request, 'competicoes/categoria.html')

def atletas_categoria(request):
    return render(request, 'competicoes/atletas_categoria.html')

def chaveamento_kata(request):
    return render(request, 'competicoes/chaveamento_kata.html')