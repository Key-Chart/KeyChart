from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Competicao, Categoria, Academia
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

# Função para criar Competições
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
            return redirect('competicoes:home')

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
    return redirect('competicoes:home')

# Função para Atualizar Competição
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
        if not nome or not modalidade or not data_inicio or not horario or not local:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('competicoes:home')
        if len(nome) < 3:
            messages.error(request, 'Nome da competição muito curto.')
            return redirect('competicoes:home')
        competicao.nome = nome
        competicao.modalidade = modalidade
        competicao.data_inicio = data_inicio
        competicao.horario = horario
        competicao.local = local
        competicao.arbitros = arbitros
        competicao.regras_especificas = regras_especificas
        competicao.status = status
        competicao.save()
        messages.success(request, 'Competição atualizada com sucesso!')
        return redirect('competicoes:home')
    return redirect('competicoes:home')

# Função para Excluir Competição
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
    return redirect('competicoes:home')

# Função para Listar todas as Competições
def listar_competicoes(request):
    competicoes = Competicao.objects.all().order_by('-data_inicio')
    search_query = request.GET.get('q')
    if search_query:
        competicoes = competicoes.filter(
            Q(nome__icontains=search_query) |
            Q(local__icontains=search_query) |
            Q(modalidade__icontains=search_query) |
            Q(arbitros__icontains=search_query)
        )
    if 'status' in request.GET and request.GET['status']:
        competicoes = competicoes.filter(status=request.GET['status'])
    date_filter = request.GET.get('data')
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            competicoes = competicoes.filter(data_inicio__date=date_obj)
        except (ValueError, TypeError):
            pass
    context = {
        'listar_competicoes': competicoes,
        'status_choices': ['Ativa', 'Finalizada', 'Em breve'],
    }
    return render(request, 'competicoes/competicoes.html', context)

# Função da rota principal da página Competições
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

# Função principal da tela de Categoria
def categoria(request, competicao_id):
    competicao = Competicao.objects.get(id=competicao_id)
    categorias = Categoria.objects.filter(competicao=competicao)
    academias = Academia.objects.all()
    if request.method == 'POST' and 'categoria_submit' in request.POST:
        try:
            nome = request.POST.get('nome')
            sexo = request.POST.get('sexo')
            tipo = request.POST.get('tipo')
            Categoria.objects.create(
                competicao=competicao,
                nome=nome,
                sexo=sexo,
                tipo=tipo
            )
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categoria', competicao_id=competicao_id)
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar categoria: {str(e)}')

    # Processar formulário de academia
    if request.method == 'POST' and 'academia_submit' in request.POST:
        try:
            nome = request.POST.get('academyName')
            cidade = request.POST.get('academyCity')
            estado = request.POST.get('academyState')
            endereco = request.POST.get('academyAddress')

            # Criar nova academia
            Academia.objects.create(
                nome=nome,
                cidade=cidade,
                estado=estado,
                endereco=endereco
            )
            messages.success(request, 'Academia cadastrada com sucesso!')
            return redirect('categoria', competicao_id=competicao_id)
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar academia: {str(e)}')

    context = {
        'competicao': competicao,
        'categorias': categorias,
        'academias': academias,
    }
    return render(request, 'competicoes/categoria.html', context)

# Função para Excluir Categoria
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    competicao_id = categoria.competicao.id
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('categoria', competicao_id=competicao_id)

# Função para Editar Academia
def editar_academia(request, academia_id):
    academia = get_object_or_404(Academia, id=academia_id)
    if request.method == 'POST':
        academia.nome = request.POST.get('nome')
        academia.cidade = request.POST.get('cidade')
        academia.estado = request.POST.get('estado')
        academia.endereco = request.POST.get('endereco')
        academia.save()
        messages.success(request, 'Academia atualizada com sucesso!')
    return redirect('categoria', competicao_id=1)

# Função para Excluir Academia
def excluir_academia(request, academia_id):
    academia = get_object_or_404(Academia, id=academia_id)
    if request.method == 'POST':
        academia.delete()
        messages.success(request, 'Academia excluída com sucesso!')
    return redirect('categoria', competicao_id=1)

def categoria_home(request):
    # Lógica para quando não há competicao_id
    return render(request, 'competicoes/categoria.html')

# Função responsavel por renderizar a pagina de Atletas
def atletas_categoria(request):
    return render(request, 'competicoes/atletas_categoria.html')

# Função responsavel por renderizar a pagina de Chaveamento
def chaveamento_kata(request):
    return render(request, 'competicoes/chaveamento_kata.html')
