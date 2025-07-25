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
from .models import ResultadoKata, ChaveamentoKumite, PartidaKumite, PontuacaoKumite
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Competicao, Categoria, Academia, Arbitro
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
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

# Função para criar Competições
def criar_competicao(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Informações básicas
                nome_competicao = request.POST.get('nome')
                modalidade = request.POST.get('modalidade')
                data_inicio = request.POST.get('data_inicio')
                horario = request.POST.get('horario')
                local = request.POST.get('local')
                regras_especificas = request.POST.get('regras_especificas', '')
                status = request.POST.get('status', 'Ativa')

                # Validações básicas
                if not nome_competicao or not modalidade or not data_inicio or not horario or not local:
                    messages.error(request, 'Preencha todos os campos obrigatórios.')
                    return redirect('competicoes:home')

                if len(nome_competicao) < 3:
                    messages.error(request, 'Nome da competição muito curto.')
                    return redirect('competicoes:home')

                # Configurações de inscrições
                inscricoes_status = request.POST.get('inscricoes_status', 'abertas')
                inscricoes_data_limite = request.POST.get('inscricoes_data_limite')
                inscricoes_valor = request.POST.get('inscricoes_valor', '120.00')
                inscricoes_taxa = request.POST.get('inscricoes_taxa', '0.00')
                inscricoes_desconto = request.POST.get('inscricoes_desconto', '0.00')
                
                # Métodos de pagamento
                inscricoes_pagamento_pix = request.POST.get('inscricoes_pagamento_pix') == 'on'
                inscricoes_pagamento_cartao = request.POST.get('inscricoes_pagamento_cartao') == 'on'
                inscricoes_pagamento_boleto = request.POST.get('inscricoes_pagamento_boleto') == 'on'
                
                # Configurações de exibição
                inscricoes_mostrar_valor = request.POST.get('inscricoes_mostrar_valor') == 'on'
                inscricoes_mostrar_vagas = request.POST.get('inscricoes_mostrar_vagas') == 'on'
                inscricoes_mensagem = request.POST.get('inscricoes_mensagem', '')

                # Converter valores monetários
                try:
                    inscricoes_valor = Decimal(inscricoes_valor)
                    inscricoes_taxa = Decimal(inscricoes_taxa)
                    inscricoes_desconto = Decimal(inscricoes_desconto)
                except (ValueError, TypeError):
                    messages.error(request, 'Valores monetários inválidos.')
                    return redirect('competicoes:home')

                # Converter data limite se fornecida
                inscricoes_data_limite_obj = None
                if inscricoes_data_limite:
                    try:
                        inscricoes_data_limite_obj = datetime.strptime(inscricoes_data_limite, '%Y-%m-%d').date()
                    except ValueError:
                        messages.error(request, 'Data limite das inscrições inválida.')
                        return redirect('competicoes:home')

                # Determinar se inscrições estão abertas
                inscricoes_abertas = inscricoes_status == 'abertas'

                # Criar a competição
                nova_competicao = Competicao(
                    nome=nome_competicao,
                    modalidade=modalidade,
                    data_inicio=data_inicio,
                    horario=horario,
                    local=local,
                    regras_especificas=regras_especificas,
                    status=status,
                    inscricoes_abertas=inscricoes_abertas,
                    inscricoes_status=inscricoes_status,
                    inscricoes_data_limite=inscricoes_data_limite_obj,
                    inscricoes_valor=inscricoes_valor,
                    inscricoes_taxa=inscricoes_taxa,
                    inscricoes_desconto=inscricoes_desconto,
                    inscricoes_pagamento_pix=inscricoes_pagamento_pix,
                    inscricoes_pagamento_cartao=inscricoes_pagamento_cartao,
                    inscricoes_pagamento_boleto=inscricoes_pagamento_boleto,
                    inscricoes_mostrar_valor=inscricoes_mostrar_valor,
                    inscricoes_mostrar_vagas=inscricoes_mostrar_vagas,
                    inscricoes_mensagem=inscricoes_mensagem
                )
                nova_competicao.save()

                # Processar árbitros selecionados
                arbitros_selecionados = request.POST.getlist('arbitros')
                if arbitros_selecionados:
                    arbitros_objs = Arbitro.objects.filter(id__in=arbitros_selecionados)
                    nova_competicao.arbitros.set(arbitros_objs)

                # Processar novo árbitro (se fornecido)
                novo_arbitro_nome = request.POST.get('novo_arbitro_nome', '').strip()
                novo_arbitro_email = request.POST.get('novo_arbitro_email', '').strip()
                novo_arbitro_telefone = request.POST.get('novo_arbitro_telefone', '').strip()

                if novo_arbitro_nome and novo_arbitro_email:
                    try:
                        # Verificar se já existe um árbitro com esse email
                        arbitro_existente = Arbitro.objects.filter(email=novo_arbitro_email).first()
                        if arbitro_existente:
                            # Adicionar árbitro existente à competição
                            nova_competicao.arbitros.add(arbitro_existente)
                        else:
                            # Criar novo árbitro
                            novo_arbitro = Arbitro.objects.create(
                                nome=novo_arbitro_nome,
                                email=novo_arbitro_email,
                                telefone=novo_arbitro_telefone
                            )
                            nova_competicao.arbitros.add(novo_arbitro)
                    except ValidationError as e:
                        messages.warning(request, f'Erro ao adicionar árbitro: {str(e)}')

                messages.success(request, 'Competição criada com sucesso!')
                return redirect('competicoes:home')
                
        except Exception as e:
            messages.error(request, f'Erro ao criar competição: {str(e)}')
            return redirect('competicoes:home')
            
    return redirect('competicoes:home')

# Função para Atualizar Competição
def editar_competicao(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Informações básicas
                nome = request.POST.get('nome')
                modalidade = request.POST.get('modalidade')
                data_inicio = request.POST.get('data_inicio')
                horario = request.POST.get('horario')
                local = request.POST.get('local')
                regras_especificas = request.POST.get('regras_especificas', '')
                status = request.POST.get('status')
                
                # Validações básicas
                if not nome or not modalidade or not data_inicio or not horario or not local:
                    messages.error(request, 'Preencha todos os campos obrigatórios.')
                    return redirect('competicoes:home')
                if len(nome) < 3:
                    messages.error(request, 'Nome da competição muito curto.')
                    return redirect('competicoes:home')
                
                # Configurações de inscrições
                inscricoes_status = request.POST.get('inscricoes_status', 'abertas')
                inscricoes_data_limite = request.POST.get('inscricoes_data_limite')
                inscricoes_valor = request.POST.get('inscricoes_valor', '120.00')
                inscricoes_taxa = request.POST.get('inscricoes_taxa', '0.00')
                inscricoes_desconto = request.POST.get('inscricoes_desconto', '0.00')
                
                # Métodos de pagamento
                inscricoes_pagamento_pix = request.POST.get('inscricoes_pagamento_pix') == 'on'
                inscricoes_pagamento_cartao = request.POST.get('inscricoes_pagamento_cartao') == 'on'
                inscricoes_pagamento_boleto = request.POST.get('inscricoes_pagamento_boleto') == 'on'
                
                # Configurações de exibição
                inscricoes_mostrar_valor = request.POST.get('inscricoes_mostrar_valor') == 'on'
                inscricoes_mostrar_vagas = request.POST.get('inscricoes_mostrar_vagas') == 'on'
                inscricoes_mensagem = request.POST.get('inscricoes_mensagem', '')

                # Converter valores monetários
                try:
                    inscricoes_valor = Decimal(inscricoes_valor)
                    inscricoes_taxa = Decimal(inscricoes_taxa)
                    inscricoes_desconto = Decimal(inscricoes_desconto)
                except (ValueError, TypeError):
                    messages.error(request, 'Valores monetários inválidos.')
                    return redirect('competicoes:home')

                # Converter data limite se fornecida
                inscricoes_data_limite_obj = None
                if inscricoes_data_limite:
                    try:
                        inscricoes_data_limite_obj = datetime.strptime(inscricoes_data_limite, '%Y-%m-%d').date()
                    except ValueError:
                        messages.error(request, 'Data limite das inscrições inválida.')
                        return redirect('competicoes:home')

                # Determinar se inscrições estão abertas
                inscricoes_abertas = inscricoes_status == 'abertas'
                
                # Atualizar competição
                competicao.nome = nome
                competicao.modalidade = modalidade
                competicao.data_inicio = data_inicio
                competicao.horario = horario
                competicao.local = local
                competicao.regras_especificas = regras_especificas
                competicao.status = status
                competicao.inscricoes_abertas = inscricoes_abertas
                competicao.inscricoes_status = inscricoes_status
                competicao.inscricoes_data_limite = inscricoes_data_limite_obj
                competicao.inscricoes_valor = inscricoes_valor
                competicao.inscricoes_taxa = inscricoes_taxa
                competicao.inscricoes_desconto = inscricoes_desconto
                competicao.inscricoes_pagamento_pix = inscricoes_pagamento_pix
                competicao.inscricoes_pagamento_cartao = inscricoes_pagamento_cartao
                competicao.inscricoes_pagamento_boleto = inscricoes_pagamento_boleto
                competicao.inscricoes_mostrar_valor = inscricoes_mostrar_valor
                competicao.inscricoes_mostrar_vagas = inscricoes_mostrar_vagas
                competicao.inscricoes_mensagem = inscricoes_mensagem
                competicao.save()
                
                # Processar árbitros selecionados
                arbitros_selecionados = request.POST.getlist('arbitros')
                if arbitros_selecionados:
                    arbitros_objs = Arbitro.objects.filter(id__in=arbitros_selecionados)
                    competicao.arbitros.set(arbitros_objs)
                else:
                    competicao.arbitros.clear()

                messages.success(request, 'Competição atualizada com sucesso!')
                return redirect('competicoes:home')
                
        except Exception as e:
            messages.error(request, f'Erro ao atualizar competição: {str(e)}')
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
    # Processar filtros de busca
    listar_competicoes = Competicao.objects.all().order_by('-data_inicio')
    search_query = request.GET.get('q')
    
    # Filtro de busca geral
    if search_query:
        listar_competicoes = listar_competicoes.filter(
            Q(nome__icontains=search_query) |
            Q(local__icontains=search_query) |
            Q(modalidade__icontains=search_query) |
            Q(arbitros__nome__icontains=search_query)
        ).distinct()
    
    # Filtro por status
    if 'status' in request.GET and request.GET['status']:
        listar_competicoes = listar_competicoes.filter(status=request.GET['status'])
    
    # Filtro por modalidade
    if 'modalidade' in request.GET and request.GET['modalidade']:
        listar_competicoes = listar_competicoes.filter(modalidade__icontains=request.GET['modalidade'])
    
    # Filtro por árbitro
    if 'arbitro' in request.GET and request.GET['arbitro']:
        listar_competicoes = listar_competicoes.filter(arbitros__id=request.GET['arbitro'])
        
    # Filtro por data
    date_filter = request.GET.get('data')
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            listar_competicoes = listar_competicoes.filter(data_inicio=date_obj)
        except (ValueError, TypeError):
            pass
    
    # Filtro por período de data
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            listar_competicoes = listar_competicoes.filter(data_inicio__gte=data_inicio_obj)
        except (ValueError, TypeError):
            pass
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            listar_competicoes = listar_competicoes.filter(data_inicio__lte=data_fim_obj)
        except (ValueError, TypeError):
            pass
    
    # Estatísticas
    total_competicoes = Competicao.objects.all().count()
    competicoes_ativas = Competicao.objects.filter(status='Ativa').count()
    competicoes_finalizadas = Competicao.objects.filter(status='Finalizada').count()
    competicoes_em_breve = Competicao.objects.filter(status='Em breve').count()
    
    # Dados para os filtros
    todos_arbitros = Arbitro.objects.all().order_by('nome')
    modalidades_distintas = Competicao.objects.values_list('modalidade', flat=True).distinct().order_by('modalidade')
    
    context = {
        'total_competicoes': total_competicoes,
        'competicoes_ativas': competicoes_ativas,
        'competicoes_finalizadas': competicoes_finalizadas,
        'competicoes_em_breve': competicoes_em_breve,
        'listar_competicoes': listar_competicoes,
        'todos_arbitros': todos_arbitros,
        'modalidades_distintas': modalidades_distintas,
        'status_choices': ['Ativa', 'Finalizada', 'Em breve'],
    }
    return render(request, 'competicoes/competicoes.html', context)

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
    from .models import ChaveamentoKata
    import json
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    atletas = Atleta.objects.filter(categoria=categoria).select_related('academia')
    
    # Cria ou obtém o chaveamento para esta categoria
    chaveamento, created = ChaveamentoKata.objects.get_or_create(
        categoria=categoria,
        defaults={'competicao': categoria.competicao}
    )
    
    # Se acabou de criar, inicializa os resultados das eliminatórias
    if created:
        with transaction.atomic():
            for atleta in atletas:
                ResultadoKata.objects.get_or_create(
                    atleta=atleta,
                    categoria=categoria,
                    fase='eliminatorias',
                    defaults={
                        'competicao': categoria.competicao,
                        'nota1': 0.0, 'nota2': 0.0, 'nota3': 0.0, 'nota4': 0.0, 'nota5': 0.0
                    }
                )
    
    # Verifica quais fases já foram salvas
    fases_salvas = {}
    for fase in ['eliminatorias', 'semifinal', 'final']:
        fases_salvas[fase] = ResultadoKata.objects.filter(
            categoria=categoria,
            fase=fase,
            salvo=True
        ).exists()
    
    # Processa requisições AJAX
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                action = data.get('action')
                
                if action == 'save_scores':
                    return handle_save_scores(request, data, categoria, chaveamento)
                elif action == 'advance_phase':
                    return handle_advance_phase(request, data, categoria, chaveamento)
                elif action == 'classify_athlete':
                    return handle_classify_athlete(request, data, categoria)
                elif action == 'eliminate_athlete':
                    return handle_eliminate_athlete(request, data, categoria)
                    
            else:  # Form data para compatibilidade
                return handle_form_submission(request, categoria, chaveamento)
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Carrega dados para o template
    context = {
        'competicao': categoria.competicao,
        'categoria': categoria,
        'atletas': atletas,
        'chaveamento': chaveamento,
        'resultados_eliminatorias': get_phase_results(categoria, 'eliminatorias'),
        'resultados_semifinal': get_phase_results(categoria, 'semifinal'),
        'resultados_final': get_phase_results(categoria, 'final'),
        'podio': chaveamento.get_podio() if chaveamento.finalizado else [],
        'cidades_distintas': atletas.values_list('cidade', flat=True).distinct().order_by('cidade'),
        'estados_distintos': atletas.values_list('estado', flat=True).distinct().order_by('estado'),
        'fases_salvas': fases_salvas,
        # Dados serializados para JavaScript
        'fases_salvas_json': json.dumps(fases_salvas),
        'resultados_eliminatorias_json': json.dumps([
            {
                'atleta': {'id': r.atleta.id},
                'nota1': float(r.nota1),
                'nota2': float(r.nota2),
                'nota3': float(r.nota3),
                'nota4': float(r.nota4),
                'nota5': float(r.nota5),
                'total': float(r.total),
                'posicao': r.posicao,
                'status': r.status,
                'salvo': r.salvo
            } for r in get_phase_results(categoria, 'eliminatorias')
        ]),
        'resultados_semifinal_json': json.dumps([
            {
                'atleta': {'id': r.atleta.id},
                'nota1': float(r.nota1),
                'nota2': float(r.nota2),
                'nota3': float(r.nota3),
                'nota4': float(r.nota4),
                'nota5': float(r.nota5),
                'total': float(r.total),
                'posicao': r.posicao,
                'status': r.status,
                'salvo': r.salvo
            } for r in get_phase_results(categoria, 'semifinal')
        ]),
        'resultados_final_json': json.dumps([
            {
                'atleta': {'id': r.atleta.id},
                'nota1': float(r.nota1),
                'nota2': float(r.nota2),
                'nota3': float(r.nota3),
                'nota4': float(r.nota4),
                'nota5': float(r.nota5),
                'total': float(r.total),
                'posicao': r.posicao,
                'status': r.status,
                'salvo': r.salvo
            } for r in get_phase_results(categoria, 'final')
        ]),
    }
    
    return render(request, 'competicoes/chaveamento_kata.html', context)


def get_phase_results(categoria, fase):
    """Retorna os resultados de uma fase específica"""
    return ResultadoKata.objects.filter(
        categoria=categoria,
        fase=fase
    ).select_related('atleta', 'atleta__academia').order_by('-total', 'posicao')


def handle_save_scores(request, data, categoria, chaveamento):
    """Salva as notas de uma fase"""
    try:
        fase = data.get('fase', 'eliminatorias')
        scores_data = data.get('scores', {})
        
        print(f"DEBUG: === INÍCIO SALVAMENTO ===")
        print(f"DEBUG: Fase: {fase}")
        print(f"DEBUG: Data completa recebida: {data}")
        print(f"DEBUG: Scores data: {scores_data}")
        print(f"DEBUG: Tipo de scores_data: {type(scores_data)}")
        print(f"DEBUG: Número de atletas a processar: {len(scores_data)}")
        
        # Verifica se há dados para processar
        if not scores_data:
            print("DEBUG: ERRO - Nenhum dado de scores recebido!")
            return JsonResponse({
                'success': False, 
                'error': 'Nenhum dado de notas foi recebido.'
            })
        
        # Verifica se a fase já foi salva
        existing_results = ResultadoKata.objects.filter(
            categoria=categoria,
            fase=fase,
            salvo=True
        ).exists()
        
        if existing_results:
            return JsonResponse({
                'success': False, 
                'error': 'Esta fase já foi salva e não pode ser alterada.'
            })
        
        with transaction.atomic():
            qualified_athletes = []
            
            for atleta_id, scores in scores_data.items():
                print(f"DEBUG: --- Processando Atleta {atleta_id} ---")
                print(f"DEBUG: Scores recebidos: {scores}")
                print(f"DEBUG: Tipo de scores: {type(scores)}")
                
                # Converte e valida cada nota
                nota1 = float(scores.get('nota1', 0)) if scores.get('nota1') else 0.0
                nota2 = float(scores.get('nota2', 0)) if scores.get('nota2') else 0.0
                nota3 = float(scores.get('nota3', 0)) if scores.get('nota3') else 0.0
                nota4 = float(scores.get('nota4', 0)) if scores.get('nota4') else 0.0
                nota5 = float(scores.get('nota5', 0)) if scores.get('nota5') else 0.0
                
                print(f"DEBUG: Notas convertidas - N1:{nota1}, N2:{nota2}, N3:{nota3}, N4:{nota4}, N5:{nota5}")
                
                resultado, created = ResultadoKata.objects.update_or_create(
                    atleta_id=atleta_id,
                    categoria=categoria,
                    fase=fase,
                    defaults={
                        'competicao': categoria.competicao,
                        'nota1': nota1,
                        'nota2': nota2,
                        'nota3': nota3,
                        'nota4': nota4,
                        'nota5': nota5,
                        'salvo': True  # Marca como salvo
                    }
                )
                
                print(f"DEBUG: Resultado salvo - Total calculado: {resultado.total}")
                print(f"DEBUG: Status do resultado: {resultado.status}")
                
                # Adiciona à lista para classificação
                qualified_athletes.append({
                    'id': int(atleta_id),
                    'total': resultado.total
                })
            
            # Atualiza posições da fase
            update_positions_for_phase(categoria, fase)
            
            # Ordena atletas por pontuação (decrescente)
            qualified_athletes.sort(key=lambda x: x['total'], reverse=True)
            
            print(f"DEBUG: Atletas ordenados: {qualified_athletes}")
            
            # Determina quantos atletas avançam baseado nas regras oficiais de Kata
            total_athletes = len(qualified_athletes)
            advance_count = 0
            
            if fase == 'eliminatorias':
                # Regras oficiais para eliminatórias de Kata
                if total_athletes <= 4:
                    # Com 4 ou menos atletas, todos vão para final
                    advance_count = total_athletes
                elif total_athletes <= 8:
                    # Com 5-8 atletas, top 4 para final
                    advance_count = min(4, total_athletes)
                elif total_athletes <= 16:
                    # Com 9-16 atletas, top 8 para semifinal
                    advance_count = min(8, total_athletes)
                else:
                    # Com mais de 16 atletas, top 16 para próxima fase
                    advance_count = min(16, total_athletes)
                    
            elif fase == 'semifinal':
                # Da semifinal sempre passam 4 para final (ou menos se houver menos competidores)
                advance_count = min(4, total_athletes)
                
            elif fase == 'final':
                # Na final, os 3 melhores vão para o pódio
                advance_count = min(3, total_athletes)
            
            print(f"DEBUG: Fase {fase} - Total atletas: {total_athletes}, Avançam: {advance_count}")
            print(f"DEBUG: Critério aplicado: Regras oficiais WKF para Kata")
            
            # Filtrar atletas com pontuação mínima (configurável)
            # Para Kata, tradicionalmente exige-se uma pontuação mínima para avançar
            # Você pode ajustar este valor conforme as regras da sua competição
            PONTUACAO_MINIMA = 5.0  # Altere aqui para ajustar a pontuação mínima
            atletas_com_pontuacao_minima = [a for a in qualified_athletes if a['total'] >= PONTUACAO_MINIMA]
            
            if len(atletas_com_pontuacao_minima) < advance_count:
                print(f"DEBUG: Apenas {len(atletas_com_pontuacao_minima)} atletas atingiram a pontuação mínima de {PONTUACAO_MINIMA}")
                advance_count = len(atletas_com_pontuacao_minima)
            
            # Aplica classificação automática
            for i, athlete in enumerate(qualified_athletes):
                atleta_id = athlete['id']
                resultado = ResultadoKata.objects.get(
                    atleta_id=atleta_id,
                    categoria=categoria,
                    fase=fase
                )
                
                # Verifica se o atleta se classifica, tem pontuação válida E atinge a pontuação mínima
                if (i < advance_count and 
                    athlete['total'] > 0 and 
                    athlete['total'] >= PONTUACAO_MINIMA):
                    resultado.status = 'classificado'
                    athlete['status'] = 'qualified'
                    print(f"DEBUG: Atleta {atleta_id} CLASSIFICADO (posição {i+1}, total {athlete['total']})")
                else:
                    resultado.status = 'eliminado'
                    athlete['status'] = 'eliminated'
                    if athlete['total'] < PONTUACAO_MINIMA:
                        print(f"DEBUG: Atleta {atleta_id} ELIMINADO por pontuação insuficiente (posição {i+1}, total {athlete['total']} < {PONTUACAO_MINIMA})")
                    else:
                        print(f"DEBUG: Atleta {atleta_id} ELIMINADO por classificação (posição {i+1}, total {athlete['total']})")
                
                resultado.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Notas da {fase} salvas com sucesso! {advance_count} atletas classificados (regras WKF Kata).',
            'qualified_athletes': qualified_athletes,
            'advance_count': advance_count,
            'total_athletes': total_athletes,
            'pontuacao_minima': 5.0,
            'criterio': 'Regras oficiais WKF para competições de Kata'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def handle_advance_phase(request, data, categoria, chaveamento):
    """Avança para a próxima fase"""
    try:
        next_phase = data.get('next_phase')
        qualified_athletes = data.get('qualified_athletes', [])
        
        with transaction.atomic():
            # Cria resultados para a próxima fase
            for atleta_id in qualified_athletes:
                ResultadoKata.objects.get_or_create(
                    atleta_id=atleta_id,
                    categoria=categoria,
                    fase=next_phase,
                    defaults={
                        'competicao': categoria.competicao,
                        'nota1': 0.0, 'nota2': 0.0, 'nota3': 0.0, 'nota4': 0.0, 'nota5': 0.0,
                        'status': 'ativo'
                    }
                )
            
            # Atualiza o chaveamento
            chaveamento.fase_atual = next_phase
            if next_phase == 'final' and len(qualified_athletes) <= 4:
                chaveamento.finalizado = True
                chaveamento.data_finalizacao = timezone.now()
            chaveamento.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{len(qualified_athletes)} atletas avançaram para {next_phase}!'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def handle_classify_athlete(request, data, categoria):
    """Classifica um atleta"""
    try:
        atleta_id = data.get('atleta_id')
        fase = data.get('fase', 'eliminatorias')
        
        resultado = ResultadoKata.objects.get(
            atleta_id=atleta_id,
            categoria=categoria,
            fase=fase
        )
        resultado.status = 'classificado'
        resultado.save()
        
        return JsonResponse({'success': True})
        
    except ResultadoKata.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Resultado não encontrado'})


def handle_eliminate_athlete(request, data, categoria):
    """Elimina um atleta"""
    try:
        atleta_id = data.get('atleta_id')
        fase = data.get('fase', 'eliminatorias')
        
        resultado = ResultadoKata.objects.get(
            atleta_id=atleta_id,
            categoria=categoria,
            fase=fase
        )
        resultado.status = 'eliminado'
        resultado.save()
        
        return JsonResponse({'success': True})
        
    except ResultadoKata.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Resultado não encontrado'})


def handle_form_submission(request, categoria, chaveamento):
    """Manipula submissões de formulário (compatibilidade)"""
    try:
        with transaction.atomic():
            atletas = Atleta.objects.filter(categoria=categoria)
            
            for atleta in atletas:
                nota1 = float(request.POST.get(f'nota1_{atleta.id}', 0))
                nota2 = float(request.POST.get(f'nota2_{atleta.id}', 0))
                nota3 = float(request.POST.get(f'nota3_{atleta.id}', 0))
                nota4 = float(request.POST.get(f'nota4_{atleta.id}', 0))
                nota5 = float(request.POST.get(f'nota5_{atleta.id}', 0))
                
                ResultadoKata.objects.update_or_create(
                    atleta=atleta,
                    categoria=categoria,
                    fase='eliminatorias',
                    defaults={
                        'nota1': nota1, 'nota2': nota2, 'nota3': nota3,
                        'nota4': nota4, 'nota5': nota5,
                        'competicao': categoria.competicao
                    }
                )
            
            update_positions_for_phase(categoria, 'eliminatorias')
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def update_positions_for_phase(categoria, fase):
    """Atualiza as posições dos atletas em uma fase"""
    resultados = ResultadoKata.objects.filter(
        categoria=categoria,
        fase=fase
    ).order_by('-total')
    
    for index, resultado in enumerate(resultados, 1):
        resultado.posicao = index
        resultado.save(update_fields=['posicao'])

# Função para chaveamento Kumitê
def chaveamento_kumite(request, categoria_id):
    from .models import ChaveamentoKumite, PartidaKumite, PontuacaoKumite
    import json
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    atletas = Atleta.objects.filter(categoria=categoria).select_related('academia')
    
    # Cria ou obtém o chaveamento para esta categoria
    chaveamento, created = ChaveamentoKumite.objects.get_or_create(
        categoria=categoria,
        defaults={
            'competicao': categoria.competicao,
            'tipo_chaveamento': 'eliminacao_simples'
        }
    )
    
    # Se acabou de criar, inicializa as partidas
    if created:
        inicializar_chaveamento_kumite(chaveamento, atletas)
    
    # Processa requisições AJAX
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                action = data.get('action')
                
                if action == 'finalizar_partida':
                    return handle_finalizar_partida(request, data, categoria, chaveamento)
                elif action == 'avancar_fase':
                    return handle_avancar_fase_kumite(request, data, categoria, chaveamento)
                elif action == 'registrar_pontuacao':
                    return handle_registrar_pontuacao(request, data, categoria)
                    
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Dados JSON inválidos'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Obtém todas as partidas organizadas por fase
    partidas_por_fase = {}
    fases = chaveamento.determinar_fases()
    
    for fase in fases:
        partidas = PartidaKumite.objects.filter(
            chaveamento=chaveamento,
            fase=fase
        ).order_by('round_numero')
        partidas_por_fase[fase] = partidas
    
    # Contar partidas finalizadas para determinar se pode mostrar chaveamento completo
    total_partidas = PartidaKumite.objects.filter(chaveamento=chaveamento).count()
    partidas_finalizadas = PartidaKumite.objects.filter(
        chaveamento=chaveamento,
        status='finalizada'
    ).count()
    partidas_pendentes = total_partidas - partidas_finalizadas
    
    # Pelo menos 50% das partidas devem estar finalizadas para mostrar chaveamento completo
    pode_mostrar_chaveamento_completo = (
        total_partidas > 0 and 
        (partidas_finalizadas / total_partidas) >= 0.5
    ) or chaveamento.finalizado

    # Dados para o template
    context = {
        'competicao': categoria.competicao,
        'categoria': categoria,
        'chaveamento': chaveamento,
        'atletas': atletas,
        'partidas_por_fase': partidas_por_fase,
        'fases': fases,
        'fase_atual': chaveamento.fase_atual,
        'num_atletas': atletas.count(),
        'finalizado': chaveamento.finalizado,
        'total_partidas': total_partidas,
        'partidas_finalizadas': partidas_finalizadas,
        'partidas_pendentes': partidas_pendentes,
        'pode_mostrar_chaveamento_completo': pode_mostrar_chaveamento_completo,
    }
    
    return render(request, 'competicoes/chaveamento_kumite.html', context)


def chaveamento_kumite_dados(request, categoria_id):
    """Retorna os dados do chaveamento no formato esperado pelo gracket.js"""
    from .models import ChaveamentoKumite, PartidaKumite
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    try:
        chaveamento = ChaveamentoKumite.objects.get(categoria=categoria)
        partidas = PartidaKumite.objects.filter(chaveamento=chaveamento).order_by('fase', 'round_numero')
        
        # Organiza os dados no formato esperado pelo gracket.js
        dados_gracket = organizar_dados_gracket(partidas)
        
        # Cria labels das rodadas baseado nas fases reais do chaveamento
        fases_chaveamento = chaveamento.determinar_fases()
        round_labels = []
        
        # Mapeamento de nomes das fases para labels amigáveis
        fase_labels = {
            'primeira_fase': 'Primeira Fase',
            'oitavas': 'Oitavas de Final',
            'quartas': 'Quartas de Final',
            'semifinal': 'Semifinais',
            'final': 'Final'
        }
        
        # Adiciona labels baseado nas fases do chaveamento
        for fase in fases_chaveamento:
            if fase in fase_labels:
                round_labels.append(fase_labels[fase])
        
        # Sempre adiciona "Campeão" no final
        round_labels.append('Campeão')
        
        return JsonResponse({
            'success': True,
            'chaveamento_data': dados_gracket,
            'round_labels': round_labels
        })
        
    except ChaveamentoKumite.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Chaveamento não encontrado para esta categoria'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro ao carregar dados: {str(e)}'
        })


def organizar_dados_gracket(partidas):
    """Organiza as partidas no formato esperado pelo gracket.js"""
    if not partidas:
        return []
    
    # Agrupa partidas por fase
    dados_por_fase = {}
    chaveamento = None
    for partida in partidas:
        fase = partida.fase
        if fase not in dados_por_fase:
            dados_por_fase[fase] = []
        dados_por_fase[fase].append(partida)
        if chaveamento is None:
            chaveamento = partida.chaveamento
    
    resultado = []
    
    # Primeira rodada - sempre a primeira_fase com todos os atletas
    if 'primeira_fase' in dados_por_fase:
        round_data = []
        partidas_fase = sorted(dados_por_fase['primeira_fase'], key=lambda x: x.round_numero)
        
        for partida in partidas_fase:
            match_data = []
            
            # Adiciona atleta 1 se existir
            if partida.atleta1:
                atleta1_data = {
                    'name': partida.atleta1.nome_completo,
                    'id': f'atleta-{partida.atleta1.id}',
                    'seed': partida.round_numero * 2 - 1,
                    'score': partida.pontos_atleta1 if partida.status == 'finalizada' and partida.pontos_atleta1 is not None else 0
                }
                match_data.append(atleta1_data)
            
            # Adiciona atleta 2 se existir
            if partida.atleta2:
                atleta2_data = {
                    'name': partida.atleta2.nome_completo,
                    'id': f'atleta-{partida.atleta2.id}',
                    'seed': partida.round_numero * 2,
                    'score': partida.pontos_atleta2 if partida.status == 'finalizada' and partida.pontos_atleta2 is not None else 0
                }
                match_data.append(atleta2_data)
            
            if match_data:
                round_data.append(match_data)
        
        if round_data:
            resultado.append(round_data)
            
            # Obtem as fases reais do chaveamento, excluindo a primeira_fase
            if chaveamento:
                fases_chaveamento = chaveamento.determinar_fases()
                fases_ordem = [fase for fase in fases_chaveamento if fase != 'primeira_fase']
            else:
                # Fallback caso não consiga obter o chaveamento
                fases_ordem = ['semifinal', 'final']
            
            num_jogos_atual = len(round_data) // 2
            
            for i, fase in enumerate(fases_ordem):
                if num_jogos_atual < 1:
                    break
                    
                round_data = []
                
                if fase in dados_por_fase:
                    # Se há dados reais para esta fase
                    partidas_fase = sorted(dados_por_fase[fase], key=lambda x: x.round_numero)
                    
                    for partida in partidas_fase:
                        match_data = []
                        
                        # Adiciona atleta1 se existir
                        if partida.atleta1:
                            atleta1_data = {
                                'name': partida.atleta1.nome_completo,
                                'id': f'atleta-{partida.atleta1.id}',
                                'seed': partida.round_numero * 2 - 1,
                                'score': partida.pontos_atleta1 if partida.status == 'finalizada' and partida.pontos_atleta1 is not None else 0
                            }
                            match_data.append(atleta1_data)
                        
                        # Adiciona atleta2 se existir
                        if partida.atleta2:
                            atleta2_data = {
                                'name': partida.atleta2.nome_completo,
                                'id': f'atleta-{partida.atleta2.id}',
                                'seed': partida.round_numero * 2,
                                'score': partida.pontos_atleta2 if partida.status == 'finalizada' and partida.pontos_atleta2 is not None else 0
                            }
                            match_data.append(atleta2_data)
                        elif partida.atleta1:
                            # Se só tem atleta1, adiciona um placeholder para o segundo
                            placeholder_data = {
                                'name': 'Aguardando...',
                                'id': f'aguardando-{fase}-{partida.round_numero}-2',
                                'seed': partida.round_numero * 2,
                                'score': 0
                            }
                            match_data.append(placeholder_data)
                        
                        if match_data:
                            round_data.append(match_data)
                else:
                    # Se não há dados, cria placeholders para os confrontos
                    for j in range(num_jogos_atual):
                        match_data = []
                        
                        # Adiciona dois placeholders por confronto
                        for k in range(2):
                            placeholder_data = {
                                'name': 'Aguardando...',
                                'id': f'placeholder-{fase}-{j+1}-{k+1}',
                                'seed': (j * 2) + k + 1,
                                'score': 0
                            }
                            match_data.append(placeholder_data)
                        
                        round_data.append(match_data)
                
                if round_data:
                    resultado.append(round_data)
                    num_jogos_atual = max(1, len(round_data) // 2)
            
            # Adiciona rodada do campeão
            if 'final' in dados_por_fase:
                partida_final = next((p for p in dados_por_fase['final'] if p.status == 'finalizada'), None)
                if partida_final and partida_final.vencedor:
                    campeao_data = [{
                        'name': f'🏆 {partida_final.vencedor.nome_completo}',
                        'id': f'campeao-{partida_final.vencedor.id}',
                        'seed': 1,
                        'score': partida_final.pontos_atleta1 if partida_final.vencedor == partida_final.atleta1 else partida_final.pontos_atleta2
                    }]
                    resultado.append([campeao_data])
                else:
                    # Placeholder para campeão
                    resultado.append([[{
                        'name': '🏆 Campeão',
                        'id': 'campeao-placeholder',
                        'seed': 1,
                        'score': 0
                    }]])
    
    return resultado


def inicializar_chaveamento_kumite(chaveamento, atletas):
    """Inicializa o chaveamento de kumitê com as partidas da primeira fase"""
    with transaction.atomic():
        atletas_list = list(atletas)
        random.shuffle(atletas_list)
        
        # Sempre começar com a primeira fase para mostrar o chaveamento completo
        primeira_fase = 'primeira_fase'
        
        chaveamento.fase_atual = primeira_fase
        chaveamento.save()
        
        # Cria as partidas da primeira fase
        partidas_criadas = 0
        i = 0
        while i < len(atletas_list):
            atleta1 = atletas_list[i] if i < len(atletas_list) else None
            atleta2 = atletas_list[i + 1] if i + 1 < len(atletas_list) else None
            
            if atleta1:  # Só cria partida se há pelo menos um atleta
                partida = PartidaKumite.objects.create(
                    chaveamento=chaveamento,
                    categoria=chaveamento.categoria,
                    competicao=chaveamento.competicao,
                    fase=primeira_fase,
                    round_numero=partidas_criadas + 1,
                    atleta1=atleta1,
                    atleta2=atleta2,
                    status='agendada'
                )
                partidas_criadas += 1
            
            i += 2


def handle_finalizar_partida(request, data, categoria, chaveamento):
    """Finaliza uma partida e registra o resultado"""
    try:
        partida_id = data.get('partida_id')
        resultado = data.get('resultado')
        pontos_atleta1 = data.get('pontos_atleta1', 0)
        pontos_atleta2 = data.get('pontos_atleta2', 0)
        advertencias_atleta1 = data.get('advertencias_atleta1', 0)
        advertencias_atleta2 = data.get('advertencias_atleta2', 0)
        observacoes = data.get('observacoes', '')
        
        partida = get_object_or_404(PartidaKumite, id=partida_id, chaveamento=chaveamento)
        
        with transaction.atomic():
            partida.status = 'finalizada'
            partida.resultado = resultado
            partida.pontos_atleta1 = pontos_atleta1
            partida.pontos_atleta2 = pontos_atleta2
            partida.advertencias_atleta1 = advertencias_atleta1
            partida.advertencias_atleta2 = advertencias_atleta2
            partida.observacoes = observacoes
            partida.data_fim = timezone.now()
            
            # Determina o vencedor
            partida.determinar_vencedor()
            partida.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Partida finalizada com sucesso!',
            'vencedor': partida.vencedor.nome_completo if partida.vencedor else 'Empate'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def handle_avancar_fase_kumite(request, data, categoria, chaveamento):
    """Avança para a próxima fase do kumitê"""
    try:
        fase_atual = chaveamento.fase_atual
        proxima_fase = chaveamento.get_proximo_fase(fase_atual)
        
        if not proxima_fase:
            return JsonResponse({'success': False, 'error': 'Não há próxima fase'})
        
        # Verifica se todas as partidas da fase atual foram finalizadas
        partidas_pendentes = PartidaKumite.objects.filter(
            chaveamento=chaveamento,
            fase=fase_atual,
            status__in=['agendada', 'em_andamento']
        ).count()
        
        if partidas_pendentes > 0:
            return JsonResponse({
                'success': False, 
                'error': f'Ainda há {partidas_pendentes} partidas pendentes na fase atual'
            })
        
        # Obtém os vencedores da fase atual
        vencedores = []
        partidas_fase_atual = PartidaKumite.objects.filter(
            chaveamento=chaveamento,
            fase=fase_atual,
            status='finalizada'
        ).order_by('round_numero')
        
        for partida in partidas_fase_atual:
            if partida.vencedor:
                vencedores.append(partida.vencedor)
        
        # Cria as partidas da próxima fase
        with transaction.atomic():
            partidas_criadas = 0
            i = 0
            while i < len(vencedores):
                atleta1 = vencedores[i] if i < len(vencedores) else None
                atleta2 = vencedores[i + 1] if i + 1 < len(vencedores) else None
                
                if atleta1:
                    PartidaKumite.objects.create(
                        chaveamento=chaveamento,
                        categoria=chaveamento.categoria,
                        competicao=chaveamento.competicao,
                        fase=proxima_fase,
                        round_numero=partidas_criadas + 1,
                        atleta1=atleta1,
                        atleta2=atleta2,
                        status='agendada'
                    )
                    partidas_criadas += 1
                
                i += 2
            
            # Atualiza a fase atual do chaveamento
            chaveamento.fase_atual = proxima_fase
            if proxima_fase == 'final':
                # Verifica se é a última fase
                partidas_final = PartidaKumite.objects.filter(
                    chaveamento=chaveamento,
                    fase='final'
                ).count()
                if partidas_final == 1:
                    chaveamento.finalizado = True
                    chaveamento.data_finalizacao = timezone.now()
            
            chaveamento.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Avançado para {proxima_fase}. {partidas_criadas} partidas criadas.',
            'proxima_fase': proxima_fase,
            'partidas_criadas': partidas_criadas
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def handle_registrar_pontuacao(request, data, categoria):
    """Registra pontuação durante uma partida"""
    try:
        partida_id = data.get('partida_id')
        atleta_id = data.get('atleta_id')
        tipo_pontuacao = data.get('tipo')
        pontos = data.get('pontos', 0)
        observacoes = data.get('observacoes', '')
        
        partida = get_object_or_404(PartidaKumite, id=partida_id)
        atleta = get_object_or_404(Atleta, id=atleta_id)
        
        # Cria o registro de pontuação
        PontuacaoKumite.objects.create(
            partida=partida,
            atleta=atleta,
            tipo=tipo_pontuacao,
            pontos=pontos,
            observacoes=observacoes
        )
        
        # Atualiza os pontos na partida
        if atleta == partida.atleta1:
            partida.pontos_atleta1 += pontos
        elif atleta == partida.atleta2:
            partida.pontos_atleta2 += pontos
        
        partida.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Pontuação registrada com sucesso!',
            'pontos_totais': partida.pontos_atleta1 if atleta == partida.atleta1 else partida.pontos_atleta2
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def chaveamento_kumite_teste(request):
    return render(request, 'competicoes/chaveamento_kumite_teste.html')

# ======================== VIEWS PARA GERENCIAMENTO DE ÁRBITROS ========================

def adicionar_arbitro(request):
    """View para adicionar um novo árbitro via AJAX"""
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome', '').strip()
            email = request.POST.get('email', '').strip()
            telefone = request.POST.get('telefone', '').strip()
            
            if not nome or not email:
                return JsonResponse({
                    'success': False,
                    'message': 'Nome e email são obrigatórios.'
                })
            
            # Verificar se já existe um árbitro com esse email
            if Arbitro.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Já existe um árbitro cadastrado com este email.'
                })
            
            # Criar novo árbitro
            novo_arbitro = Arbitro.objects.create(
                nome=nome,
                email=email,
                telefone=telefone
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Árbitro adicionado com sucesso!',
                'arbitro': {
                    'id': novo_arbitro.id,
                    'nome': novo_arbitro.nome,
                    'email': novo_arbitro.email,
                    'telefone': novo_arbitro.telefone
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao adicionar árbitro: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})

def adicionar_arbitro_competicao(request, competicao_id):
    """View para adicionar um árbitro a uma competição específica"""
    if request.method == 'POST':
        try:
            competicao = get_object_or_404(Competicao, id=competicao_id)
            
            # Verificar se é para adicionar um árbitro existente
            arbitro_id = request.POST.get('arbitro_id')
            if arbitro_id:
                arbitro = get_object_or_404(Arbitro, id=arbitro_id)
                
                # Verificar se o árbitro já está na competição
                if competicao.arbitros.filter(id=arbitro.id).exists():
                    return JsonResponse({
                        'success': False,
                        'message': 'Este árbitro já está cadastrado nesta competição.'
                    })
                
                # Adicionar árbitro existente à competição
                competicao.arbitros.add(arbitro)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Árbitro adicionado à competição com sucesso!',
                    'arbitro': {
                        'id': arbitro.id,
                        'nome': arbitro.nome,
                        'email': arbitro.email,
                        'telefone': arbitro.telefone
                    }
                })
            
            # Caso contrário, criar um novo árbitro
            nome = request.POST.get('nome', '').strip()
            email = request.POST.get('email', '').strip()
            telefone = request.POST.get('telefone', '').strip()
            
            if not nome or not email:
                return JsonResponse({
                    'success': False,
                    'message': 'Nome e email são obrigatórios.'
                })
            
            # Verificar se já existe um árbitro com esse email
            arbitro_existente = Arbitro.objects.filter(email=email).first()
            
            if arbitro_existente:
                # Verificar se o árbitro já está na competição
                if competicao.arbitros.filter(id=arbitro_existente.id).exists():
                    return JsonResponse({
                        'success': False,
                        'message': 'Este árbitro já está cadastrado nesta competição.'
                    })
                
                # Adicionar árbitro existente à competição
                competicao.arbitros.add(arbitro_existente)
                novo_arbitro = arbitro_existente
            else:
                # Criar novo árbitro e adicionar à competição
                novo_arbitro = Arbitro.objects.create(
                    nome=nome,
                    email=email,
                    telefone=telefone
                )
                competicao.arbitros.add(novo_arbitro)
            
            return JsonResponse({
                'success': True,
                'message': 'Árbitro adicionado à competição com sucesso!',
                'arbitro': {
                    'id': novo_arbitro.id,
                    'nome': novo_arbitro.nome,
                    'email': novo_arbitro.email,
                    'telefone': novo_arbitro.telefone
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao adicionar árbitro: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})

def remover_arbitro_competicao(request, competicao_id, arbitro_id):
    """View para remover um árbitro de uma competição específica"""
    if request.method == 'POST':
        try:
            competicao = get_object_or_404(Competicao, id=competicao_id)
            arbitro = get_object_or_404(Arbitro, id=arbitro_id)
            
            # Verificar se o árbitro está na competição
            if not competicao.arbitros.filter(id=arbitro_id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este árbitro não está cadastrado nesta competição.'
                })
            
            # Remover árbitro da competição
            competicao.arbitros.remove(arbitro)
            
            return JsonResponse({
                'success': True,
                'message': 'Árbitro removido da competição com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao remover árbitro: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})

def listar_arbitros(request):
    """View para listar todos os árbitros (para uso em AJAX)"""
    arbitros = Arbitro.objects.all().order_by('nome')
    arbitros_data = []
    
    for arbitro in arbitros:
        arbitros_data.append({
            'id': arbitro.id,
            'nome': arbitro.nome,
            'email': arbitro.email,
            'telefone': arbitro.telefone
        })
    
    return JsonResponse({
        'success': True,
        'arbitros': arbitros_data
    })


def chaveamento_kata_pdf(request, categoria_id):
    """Gera PDF com os resultados do chaveamento de Kata"""
    from .models import ChaveamentoKata
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    atletas = Atleta.objects.filter(categoria=categoria).select_related('academia')
    
    # Obtém o chaveamento
    try:
        chaveamento = ChaveamentoKata.objects.get(categoria=categoria)
    except ChaveamentoKata.DoesNotExist:
        # Se não existe chaveamento, cria um vazio para não quebrar
        chaveamento = None
    
    # Carrega dados organizados para o PDF
    context = {
        'competicao': categoria.competicao,
        'categoria': categoria,
        'atletas': atletas,
        'chaveamento': chaveamento,
        'resultados_eliminatorias': get_phase_results(categoria, 'eliminatorias'),
        'resultados_semifinal': get_phase_results(categoria, 'semifinal'),
        'resultados_final': get_phase_results(categoria, 'final'),
        'podio': chaveamento.get_podio() if chaveamento and chaveamento.finalizado else [],
        'data_geracao': timezone.now(),
    }
    
    # Organiza resultados por fase para o PDF
    context['fases'] = []
    
    # Eliminatórias
    if context['resultados_eliminatorias']:
        context['fases'].append({
            'nome': 'Eliminatórias',
            'resultados': context['resultados_eliminatorias']
        })
    
    # Semifinal
    if context['resultados_semifinal']:
        context['fases'].append({
            'nome': 'Semifinal',
            'resultados': context['resultados_semifinal']
        })
    
    # Final
    if context['resultados_final']:
        context['fases'].append({
            'nome': 'Final',
            'resultados': context['resultados_final']
        })
    
    # Renderiza o template HTML para PDF
    template = get_template('competicoes/chaveamento_kata_pdf.html')
    html = template.render(context)
    
    # Cria o PDF
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        # Prepara a resposta
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f'Kata_{categoria.competicao.nome}_{categoria.nome}_{timezone.now().strftime("%Y%m%d_%H%M")}.pdf'
        # Remove caracteres especiais do nome do arquivo
        filename = ''.join(c for c in filename if c.isalnum() or c in '._- ')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse(f'Erro ao gerar PDF: {pdf.err}', status=500)

def chaveamento_kumite_pdf(request, categoria_id):
    """Gera PDF do chaveamento de Kumitê"""
    try:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        chaveamento = get_object_or_404(ChaveamentoKumite, categoria=categoria)
        
        # Obtém todas as partidas organizadas por fase
        partidas_por_fase = {}
        fases = chaveamento.determinar_fases()
        
        for fase in fases:
            partidas = PartidaKumite.objects.filter(
                chaveamento=chaveamento,
                fase=fase
            ).order_by('round_numero')
            partidas_por_fase[fase] = partidas

        context = {
            'competicao': categoria.competicao,
            'categoria': categoria,
            'chaveamento': chaveamento,
            'partidas_por_fase': partidas_por_fase,
            'fases': fases,
            'data_geracao': timezone.now()
        }
        
        # Renderiza o template PDF
        template = get_template('competicoes/chaveamento_kumite_pdf.html')
        html = template.render(context)
        
        # Cria o PDF
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Kumite_{categoria.competicao.nome}_{categoria.nome}.pdf"'
            return response
        else:
            return HttpResponse('Erro ao gerar PDF', status=500)
            
    except Exception as e:
        return HttpResponse(f'Erro: {str(e)}', status=500)