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
def finalizar_inscricao(request):
    try:
        # Dados básicos obrigatórios
        competicao_id = request.POST.get('competicao_id')
        categoria_id = request.POST.get('categoria_id')
        nome_academia = request.POST.get('academia', '').strip()
        cidade_academia = request.POST.get('cidade', '').strip()
        estado_academia = request.POST.get('estado', '').upper()[:2]

        if not all([competicao_id, categoria_id, nome_academia, cidade_academia, estado_academia]):
            raise ValueError("Todos os campos da academia são obrigatórios: nome, cidade e estado")

        # Dados obrigatórios do atleta
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

        # 1. Obter a competição
        competicao = get_object_or_404(Competicao, pk=competicao_id)

        # 2. Buscar ou criar a academia PARA ESTA COMPETIÇÃO
        academia, created = Academia.objects.get_or_create(
            nome=nome_academia,
            competicao=competicao,
            defaults={
                'cidade': cidade_academia,
                'estado': estado_academia,
                'endereco': request.POST.get('endereco', '')
            }
        )

        # 3. Criar o atleta com os dados corretos
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
            # Você pode querer renomear o arquivo para incluir o ID do atleta
            # Mas como o ID ainda não existe, faremos isso depois do save

        atleta.full_clean()
        atleta.save()

        # D renomear o arquivo
        if atleta.foto:
            import os
            from django.conf import settings

            ext = os.path.splitext(atleta.foto.name)[1]
            new_name = f'atletas/fotos/{atleta.id}{ext}'
            old_path = atleta.foto.path
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            os.rename(old_path, new_path)
            atleta.foto.name = new_name
            atleta.save()

        # Resposta de sucesso
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

@csrf_exempt
def enviar_email_inscricao(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Renderizar o template HTML do email
            context = {
                'nome_atleta': data['nome_atleta'],
                'competicao': data['competicao'],
                'categoria': data['categoria'],
                'data_nascimento': data['data_nascimento'],
                'sexo': data['sexo'],
                'faixa': data['faixa'],
                'academia': data['academia'],
            }

            html_content = render_to_string('atletas/email_inscricao.html', context)

            # Criar e enviar o email
            email = EmailMessage(
                subject=data['assunto'],
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[data['email_destino']],
            )
            email.content_subtype = "html"
            email.send()

            return JsonResponse({
                'success': True,
                'message': 'Email enviado com sucesso!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
                'message': 'Erro ao enviar email'
            })

    return JsonResponse({
        'success': False,
        'error': 'Método não permitido',
        'message': 'Requisição inválida'
    })

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

    context = {
        'atletas': atletas,
        'filterName': nome,
        'filterAge': idade,
        'filterCategory': categoria
    }

    return render(request, 'atletas/equipes_atletas.html', context)

# Função para desativar Atleta
def desativar_atleta(request):
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

    return redirect('equipes_atletas:atletas')

# Função para Ativar atleta
def ativar_atleta(request):
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

    return redirect('equipes_atletas:atletas')


def editar_atleta(request, atleta_id):
    pass