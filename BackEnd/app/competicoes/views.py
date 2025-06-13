from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Competicao, Categoria, Academia
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from app.atletas.models import Atleta
from django.contrib import messages
import random
import math
from django.db import transaction
from .models import ResultadoKata
from django.http.response import HttpResponse, JsonResponse
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

# Função para cadastrar Acadêmia
def cadastrar_academia(request):
    if request.method == 'POST':
        competicao_id = request.POST.get('competicao_id')
        nome = request.POST.get('nome')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        endereco = request.POST.get('endereco', '')

        if not all([competicao_id, nome, cidade, estado]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('competicoes:categoria', competicao_id=competicao_id)

        try:
            competicao = get_object_or_404(Competicao, id=competicao_id)
            Academia.objects.create(
                competicao=competicao,
                nome=nome,
                cidade=cidade,
                estado=estado,
                endereco=endereco
            )
            messages.success(request, 'Academia cadastrada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')

        return redirect('competicoes:categoria', competicao_id=competicao_id)

# Função para editar Acadêmia
def editar_academia(request, academia_id):
    academia = get_object_or_404(Academia, id=academia_id)

    if request.method == 'POST':
        academia.nome = request.POST.get('nome')
        academia.cidade = request.POST.get('cidade')
        academia.estado = request.POST.get('estado')
        academia.endereco = request.POST.get('endereco', '')
        academia.save()
        messages.success(request, 'Academia atualizada com sucesso!')

    return redirect('competicoes:categoria', competicao_id=academia.competicao.id)

# Função para excluir Acadêmia
def excluir_academia(request, academia_id):
    academia = get_object_or_404(Academia, id=academia_id)
    competicao_id = academia.competicao.id

    if request.method == 'POST':
        academia.delete()
        messages.success(request, 'Academia excluída com sucesso!')

    return redirect('competicoes:categoria', competicao_id=competicao_id)

# função para cadastrar categorias para cada competição
def cadastrar_categoria(request, competicao_id):
    if request.method == 'POST' and 'categoria_submit' in request.POST:
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        tipo = request.POST.get('tipo')

        competicao = get_object_or_404(Competicao, id=competicao_id)

        categoria = Categoria.objects.create(
            nome=nome,
            sexo=sexo,
            tipo=tipo,
            competicao=competicao
        )
        messages.success(request, f'Categoria "{nome}" cadastrada com sucesso!')
        return redirect('competicoes:categoria', competicao_id=competicao.id)

# Função para listar todas as competições cadastradas
def listar_categorias(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    categorias = Categoria.objects.filter(competicao=competicao)
    return render(request, 'competicoes/listar_categorias.html', {
        'competicao': competicao,
        'categorias': categorias
    })

# Função para excluir Categoria
def excluir_categoria(request, categoria_id):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, id=categoria_id)
        nome = categoria.nome
        categoria.delete()
        messages.success(request, f'Categoria "{nome}" excluída com sucesso!')
    return redirect('competicoes:categoria', competicao_id=categoria.competicao.id)

def categoria_home(request):
    # Lógica para quando não há competicao_id
    return render(request, 'competicoes/categoria.html')

# Função responsavel por renderizar a pagina de Atletas
def atletas_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Filtre os atletas que têm essa categoria definida
    atletas = Atleta.objects.filter(categoria__id=categoria_id).select_related('academia')

    # Para debug - imprima no console
    print(f"Total de atletas encontrados: {atletas.count()}")
    for atleta in atletas:
        print(f"Atleta: {atleta.nome_completo}, Categoria: {atleta.categoria.nome if atleta.categoria else 'Nenhuma'}")

    # Para os filtros
    cidades_distintas = atletas.order_by('cidade').values_list('cidade', flat=True).distinct()
    estados_distintos = atletas.order_by('estado').values_list('estado', flat=True).distinct()

    context = {
        'categoria': categoria,
        'competicao': categoria.competicao,
        'atletas': atletas,
        'cidades_distintas': cidades_distintas,
        'estados_distintos': estados_distintos,
    }
    return render(request, 'competicoes/atletas_categoria.html', context)

def editar_atleta(request, pk):
    atleta = get_object_or_404(Atleta, pk=pk)

    if request.method == 'POST':
        # Processamento manual dos dados do formulário
        atleta.nome_completo = request.POST.get('nome_completo')
        atleta.data_nascimento = request.POST.get('data_nascimento')
        # Atualize todos os campos necessários...
        atleta.save()
        messages.success(request, 'Atleta atualizado com sucesso!')
        return redirect('competicoes:atletas_categoria', categoria_id=atleta.categoria.id)

    context = {'atleta': atleta}
    return render(request, 'atletas/editar_atleta.html', context)

def excluir_atleta(request, pk):
    atleta = get_object_or_404(Atleta, pk=pk)
    categoria_id = atleta.categoria.id
    atleta.delete()
    messages.success(request, 'Atleta excluído com sucesso!')
    return redirect('competicoes:atletas_categoria', categoria_id=categoria_id)

# Função responsavel por renderizar a pagina de Chaveamento
def chaveamento_kata(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    atletas = Atleta.objects.filter(categoria=categoria).select_related('academia')

    # Verifica se TODOS os atletas já têm resultados (para o chaveamento completo)
    chaveamento_existente = ResultadoKata.objects.filter(categoria=categoria).count() == atletas.count()

    # Para os filtros
    cidades_distintas = atletas.order_by('cidade').values_list('cidade', flat=True).distinct()
    estados_distintos = atletas.order_by('estado').values_list('estado', flat=True).distinct()

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Processa requisições AJAX individuais
        atleta_id = request.POST.get('atleta_id')
        atleta = get_object_or_404(Atleta, id=atleta_id)

        nota1 = float(request.POST.get('nota1', 0))
        nota2 = float(request.POST.get('nota2', 0))
        nota3 = float(request.POST.get('nota3', 0))
        nota4 = float(request.POST.get('nota4', 0))
        nota5 = float(request.POST.get('nota5', 0))

        resultado, created = ResultadoKata.objects.update_or_create(
            atleta=atleta,
            categoria=categoria,
            defaults={
                'nota1': nota1,
                'nota2': nota2,
                'nota3': nota3,
                'nota4': nota4,
                'nota5': nota5,
                'competicao': categoria.competicao
            }
        )

        # Verifica novamente se todos os atletas já têm resultados
        todos_salvos = ResultadoKata.objects.filter(categoria=categoria).count() == atletas.count()

        return JsonResponse({
            'success': True,
            'total': resultado.total,
            'atleta_id': atleta_id,
            'todos_salvos': todos_salvos  # Adiciona esta informação na resposta
        })
    elif request.method == 'POST':
        # Processa o salvamento em lote
        with transaction.atomic():
            for atleta in atletas:
                nota1 = float(request.POST.get(f'nota1_{atleta.id}', 0))
                nota2 = float(request.POST.get(f'nota2_{atleta.id}', 0))
                nota3 = float(request.POST.get(f'nota3_{atleta.id}', 0))
                nota4 = float(request.POST.get(f'nota4_{atleta.id}', 0))
                nota5 = float(request.POST.get(f'nota5_{atleta.id}', 0))

                ResultadoKata.objects.update_or_create(
                    atleta=atleta,
                    categoria=categoria,
                    defaults={
                        'nota1': nota1,
                        'nota2': nota2,
                        'nota3': nota3,
                        'nota4': nota4,
                        'nota5': nota5,
                        'competicao': categoria.competicao
                    }
                )

            return JsonResponse({'success': True})

    # Carrega resultados existentes
    resultados = ResultadoKata.objects.filter(atleta__in=atletas, categoria=categoria)
    resultados_dict = {resultado.atleta_id: resultado for resultado in resultados}

    context = {
        'competicao': categoria.competicao,
        'categoria': categoria,
        'atletas': atletas,
        'cidades_distintas': cidades_distintas,
        'estados_distintos': estados_distintos,
        'resultados': resultados_dict,
        'chaveamento_existente': chaveamento_existente,
    }
    return render(request, 'competicoes/chaveamento_kata.html', context)

# Função para chaveamento Kumitê
def chaveamento_kumite(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    competicao = categoria.competicao
    atletas = list(Atleta.objects.filter(categoria=categoria))

    # Se não houver atletas, retorna com aviso
    if not atletas:
        messages.error(request, "Não há atletas cadastrados nesta categoria.")
        return render(request, 'competicoes/chaveamento_kumite.html', {
            'competicao': competicao,
            'categoria': categoria,
            'partidas': [],
            'num_atletas': 0,
            'current_phase': 1,
            'max_phases': 1,
            'fase_atual': 'Sem atletas',
            'is_final': False,
        })

    # Embaralha os atletas para criar chaveamento aleatório
    random.shuffle(atletas)
    num_atletas = len(atletas)

    # Verifica se o número de atletas é potência de 2
    if not (num_atletas & (num_atletas - 1) == 0):
        messages.warning(request, f"O número de atletas ({num_atletas}) não é uma potência de 2. Serão adicionados 'byes'.")

    # Calcula o número total de fases
    max_phases = math.ceil(math.log2(num_atletas)) + 1

    # Divide os atletas em AKA (vermelho) e AO (azul)
    metade = (num_atletas + 1) // 2
    atletas_aka = atletas[:metade]
    atletas_ao = atletas[metade:]

    # Cria as partidas da primeira fase
    partidas = []
    for i in range(max(len(atletas_aka), len(atletas_ao))):
        aka = atletas_aka[i] if i < len(atletas_aka) else None
        ao = atletas_ao[i] if i < len(atletas_ao) else None
        partidas.append({
            'numero': i + 1,
            'aka': aka,
            'ao': ao,
            'area': chr(65 + (i % 3)),  # Áreas A, B, C, etc.
        })

    # Determina o nome da fase atual
    if len(partidas) == 1:
        fase_atual = "Final"
        is_final = True
    elif len(partidas) == 2:
        fase_atual = "Semifinais"
        is_final = False
    elif len(partidas) >= 4:
        fase_atual = "Quartas de Final"
        is_final = False
    else:
        fase_atual = f"Fase {math.ceil(math.log2(len(partidas)) + 1)}"
        is_final = False

    context = {
        'competicao': competicao,
        'categoria': categoria,
        'partidas': partidas,
        'num_atletas': num_atletas,
        'current_phase': 1,
        'max_phases': max_phases,
        'fase_atual': fase_atual,
        'is_final': is_final,
    }

    return render(request, 'competicoes/chaveamento_kumite.html', context)

def chaveamento_kumite_teste(request):
    return render(request, 'competicoes/chaveamento_kumite_teste.html')