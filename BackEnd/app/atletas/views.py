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
        competicao_id = request.POST.get('competicao_id')
        categoria_id = request.POST.get('categoria_id')
        nome = request.POST.get('nome')
        nascimento = request.POST.get('nascimento')
        idade = request.POST.get('idade')
        sexo = request.POST.get('sexo')
        peso = request.POST.get('peso')
        faixa = request.POST.get('faixa')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        academia = request.POST.get('academia')
        foto_url = request.POST.get('foto_url')

        atleta = Atleta(
            competicao_id=competicao_id,
            categoria_id=categoria_id,
            nome_completo=nome,
            data_nascimento=nascimento,
            idade=float(idade) if idade else None,
            sexo=sexo,
            peso=float(peso) if peso else None,
            faixa=faixa,
            cidade=cidade,
            estado=estado,
            academia=academia,
            foto_url=foto_url
        )
        atleta.save()

        messages.success(request, 'Inscrição realizada com sucesso!')
        return redirect('equipes_atletas:inscricoes')

    except Exception as e:
        messages.error(request, f'Erro ao processar inscrição: {str(e)}')
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