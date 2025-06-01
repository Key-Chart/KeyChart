from django.shortcuts import render, redirect
from django.http import JsonResponse
from app.competicoes.models import Competicao, Categoria, Academia
from .models import Atleta
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
from datetime import date

# Função para listar todos os atletas
def atletas(request):
    return render(request, 'atletas/equipes_atletas.html')

print("Estou aqui")

# Função para renderizar a tela de perfil do atleta
def perfil_atleta(request):
    return render(request, 'atletas/perfil_atleta.html')

# Função para a renderizar a tela de inscrições
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

    # Pré-carrega academias
    todas_academias = {}
    academias = Academia.objects.filter(competicao__in=competicoes)

    for academia in academias:
        competicao_id = academia.competicao.id
        if competicao_id not in todas_academias:
            todas_academias[competicao_id] = []
        todas_academias[competicao_id].append(academia)

    context = {
        'competicoes': competicoes,
        'todas_categorias': todas_categorias,
        'todas_academias': todas_academias,
    }
    return render(request, 'atletas/inscricoes.html', context)


# Função para carregar todas as categorias
def carregar_categorias(request, competicao_id):
    try:
        categorias = Categoria.objects.filter(competicao_id=competicao_id).values(
            'id', 'nome', 'tipo', 'sexo', 'get_tipo_display', 'get_sexo_display'
        )
        academias = Academia.objects.filter(competicao_id=competicao_id).values('id', 'nome')

        return JsonResponse({
            'categorias': list(categorias),
            'academias': list(academias)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def enviar_email_inscricao(request):
    try:
        competicao_id = request.POST.get('competicao_id')
        categoria_id = request.POST.get('categoria_id')
        nome_academia = request.POST.get('academia', '').strip()
        cidade_academia = request.POST.get('cidade', '').strip()
        estado_academia = request.POST.get('estado', '').upper()[:2]

        if not all([competicao_id, categoria_id, nome_academia, cidade_academia, estado_academia]):
            raise ValueError("Todos os campos da academia são obrigatórios: nome, cidade e estado")

        nome_atleta = request.POST.get('nome', '').strip()
        data_nascimento = request.POST.get('nascimento')
        sexo = request.POST.get('sexo')
        idade = float(request.POST['idade']) if request.POST.get('idade') else None
        peso = float(request.POST['peso']) if request.POST.get('peso') else None
        faixa = request.POST.get('faixa', '')
        cidade_atleta = request.POST.get('cidade', '').strip()
        estado_atleta = request.POST.get('estado', '').upper()[:2]
        altura = int(request.POST.get('altura') or 0)
        email = request.POST.get('email', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        foto = request.POST.get('foto', '')

        # Obter a competição
        competicao = get_object_or_404(Competicao, pk=competicao_id)

        # Buscar ou criar a academia PARA ESTA COMPETIÇÃO
        academia, created = Academia.objects.get_or_create(
            nome=nome_academia,
            competicao=competicao,
            defaults={
                'cidade': cidade_academia,
                'estado': estado_academia,
                'endereco': request.POST.get('endereco', '')
            }
        )

        # Criar o atleta com os dados corretos
        atleta = Atleta(
            competicao=competicao,
            categoria_id=categoria_id,
            nome_completo=nome_atleta,
            data_nascimento=data_nascimento,
            sexo=sexo,
            idade=idade,
            peso=peso,
            faixa=faixa,
            cidade=cidade_atleta,
            estado=estado_atleta,
            academia=academia,
            altura=altura,
            email=email,
            telefone=telefone,
            foto=foto
        )

        # Processar o upload da foto
        if 'foto' in request.FILES:
            atleta.foto = request.FILES['foto']

        atleta.full_clean()
        atleta.save()

        # Renomear o arquivo da foto, se existir
        if atleta.foto:
            ext = os.path.splitext(atleta.foto.name)[1]
            new_name = f'fotos_atletas/{atleta.id}{ext}'
            old_path = atleta.foto.path
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            os.rename(old_path, new_path)
            atleta.foto.name = new_name
            atleta.save()

        # Enviar email de confirmação
        try:
            html_content = render_to_string('atletas/email_inscricao.html', {
                'nome_atleta': atleta.nome_completo,
                'competicao': competicao.nome,
                'categoria': atleta.categoria.nome,  # Ajuste se necessário
                'data_nascimento': atleta.data_nascimento.strftime('%d/%m/%Y'),
                'sexo': atleta.sexo,
                'faixa': atleta.faixa,
                'academia': atleta.academia.nome,
            })

            subject = f'Confirmação de Inscrição - {competicao.nome}'
            from_email = 'rafaelgoesti2021@gmail.com'  # Troque para o seu email
            to_email = [atleta.email]

            email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

        except Exception as e:
            print(f'Erro ao enviar e-mail: {e}')

        response_data = {
            'success': True,
            'message': 'Inscrição realizada com sucesso!',
            'atleta_id': atleta.id,
            'academia_id': academia.id
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(response_data)

        messages.success(request, response_data['message'])
        return redirect('equipes_atletas:inscricoes')

    except Exception as e:
        error_message = f"Erro ao processar inscrição: {str(e)}"
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': error_message}, status=400)

        messages.error(request, error_message)
        return redirect('equipes_atletas:inscricoes')

# Função para listar todos os atletas
def atletas(request):
    # Obter parâmetros de filtro da requisição
    nome = request.GET.get('filterName', '')
    idade = request.GET.get('filterAge', '')
    categoria = request.GET.get('filterCategory', '')

    # Construir a query de filtro
    atletas = Atleta.objects.all()

    if nome:
        atletas = atletas.filter(nome_completo__icontains=nome)
    if idade:
        atletas = atletas.filter(idade=idade)
    if categoria:
        atletas = atletas.filter(categoria__tipo=categoria)

    # Como não temos campo 'ativo', vamos considerar todos como ativos
    atletas_ativos_count = atletas.count()  # Todos são considerados ativos
    atletas_inativos_count = 0  # Não temos inativos
    kata_count = atletas.filter(categoria__tipo='kata').count()
    kumite_count = atletas.filter(categoria__tipo='kumite').count()

    context = {
        'atletas': atletas,
        'atletas_ativos_count': atletas_ativos_count,
        'atletas_inativos_count': atletas_inativos_count,
        'kata_count': kata_count,
        'kumite_count': kumite_count,
        'filterName': nome,
        'filterAge': idade,
        'filterCategory': categoria
    }

    return render(request, 'atletas/equipes_atletas.html', context)

# Função para desativar Atleta
'''def desativar_atleta(request):
    if request.method == 'POST':
        atleta_id = request.POST.get('atleta_id')
        motivo = request.POST.get('motivo', '')

        try:
            atleta = Atleta.objects.get(id=atleta_id)
            atleta.ativo = False
            atleta.motivo_inativacao = motivo
            atleta.save()

            messages.success(request, f'Atleta {atleta.nome_completo} desativado com sucesso!')
        except Atleta.DoesNotExist:
            messages.error(request, 'Atleta não encontrado!')

    return redirect('equipes_atletas:atletas')'''

# Função para Ativar atleta
'''def ativar_atleta(request):
    if request.method == 'POST':
        atleta_id = request.POST.get('atleta_id')

        try:
            atleta = Atleta.objects.get(id=atleta_id)
            atleta.ativo = True
            atleta.motivo_inativacao = ''
            atleta.save()

            messages.success(request, f'Atleta {atleta.nome_completo} ativado com sucesso!')
        except Atleta.DoesNotExist:
            messages.error(request, 'Atleta não encontrado!')

    return redirect('equipes_atletas:atletas')'''

# Função para Editar Atleta
'''def editar_atleta(request, atleta_id):
    atleta = get_object_or_404(Atleta, id=atleta_id)

    if request.method == 'POST':
        atleta.nome = request.POST.get('nome')
        atleta.email = request.POST.get('email')
        atleta.data_nascimento = request.POST.get('data_nascimento')
        atleta.sexo = request.POST.get('sexo')
        atleta.categoria = request.POST.get('categoria')
        atleta.faixa = request.POST.get('faixa')
        atleta.peso = request.POST.get('peso')
        atleta.altura = request.POST.get('altura')
        atleta.equipe_id = request.POST.get('equipe')
        atleta.save()
        return redirect('nome_da_tua_view_de_lista')  # Altere para onde deve redirecionar após editar

    context = {'atleta': atleta}
    return render(request, 'teu_template.html', context)'''

# Função para abrir a tela de visualizar atleta
def perfil_atleta(request, atleta_id):
    # Busca o atleta ou retorna 404 se não existir
    atleta = get_object_or_404(Atleta, id=atleta_id)
    # Calcula a idade
    hoje = date.today()
    idade = hoje.year - atleta.data_nascimento.year - (
                (hoje.month, hoje.day) < (atleta.data_nascimento.month, atleta.data_nascimento.day))

    # Formata a data de nascimento para exibição (dd/mm/aaaa)
    data_nascimento_formatada = atleta.data_nascimento.strftime('%d/%m/%Y')

    # Prepara o contexto com apenas os dados solicitados
    context = {
        'atleta': atleta,
        'idade': idade,
        'data_nascimento_formatada': data_nascimento_formatada,
    }

    return render(request, 'atletas/perfil_atleta.html', context)

