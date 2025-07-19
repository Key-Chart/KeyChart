from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
import json
import os
import base64
from datetime import date

from app.competicoes.models import Competicao, Categoria, Academia
from .models import Atleta, CertificadoAtleta, EstatisticaAtleta, HistoricoCompeticao
import csv

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

    # Pré-carrega e serializa academias por competição
    academias = Academia.objects.filter(competicao__in=competicoes)
    todas_academias = {}

    for academia in academias:
        competicao_id = academia.competicao.id
        if competicao_id not in todas_academias:
            todas_academias[competicao_id] = []
        todas_academias[competicao_id].append({
            'id': academia.id,
            'nome': academia.nome,
            'cidade': academia.cidade,
            'estado': academia.estado,
        })

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
        '''try:
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
            print(f'Erro ao enviar e-mail: {e}')'''

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
    export_format = request.GET.get('export')

    # Construir a query de filtro
    atletas = Atleta.objects.all()

    if nome:
        atletas = atletas.filter(nome_completo__icontains=nome)
    if idade:
        atletas = atletas.filter(idade=idade)
    if categoria:
        atletas = atletas.filter(categoria__tipo=categoria)

    # Verificar se é uma requisição de exportação
    if export_format in ['pdf', 'csv']:
        return exportar_atletas(atletas, export_format)

    # Como não temos campo 'ativo', vamos considerar todos como ativos
    atletas_ativos_count = atletas.count()
    atletas_inativos_count = 0
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

# Função para exportar lista de atletas em PDF
def exportar_atletas(queryset, format):
    if format == 'pdf':
        return exportar_pdf(queryset)
    elif format == 'csv':
        return exportar_csv(queryset)

# Exportar para PDF
def exportar_pdf(queryset):
    template_path = 'atletas/exportar_pdf.html'

    # Encontrar o arquivo usando o sistema de finders do Django
    logo_path = finders.find('competicoes/img/icone_keychart.png')

    logo_base64 = None
    if logo_path:
        try:
            with open(logo_path, "rb") as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")

    context = {
        'atletas': queryset,
        'logo_base64': logo_base64
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="atletas.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response,
        encoding='utf-8'
    )

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response

# Função para exportar para CSV
def exportar_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="atletas.csv"'

    headers = ['Nome Completo', 'Email', 'Idade', 'Categoria', 'Faixa']

    # Verifica se o modelo tem o campo equipe
    if hasattr(queryset.model, 'equipe'):
        headers.append('Equipe')

    writer = csv.writer(response)
    writer.writerow(headers)

    for atleta in queryset:
        row = [
            atleta.nome_completo,
            atleta.email or '',
            atleta.idade,
            atleta.categoria.get_tipo_display(),
            atleta.get_faixa_display() or '',
        ]

        if hasattr(atleta, 'equipe'):
            row.append(atleta.equipe.nome if atleta.equipe else '')

        writer.writerow(row)

    return response

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

# Função para exportar perfil do atleta para PDF
def exportar_perfil_pdf(request, atleta_id):
    # Busca o atleta
    atleta = get_object_or_404(Atleta, id=atleta_id)
    
    # Calcula a idade
    hoje = date.today()
    idade = hoje.year - atleta.data_nascimento.year - (
        (hoje.month, hoje.day) < (atleta.data_nascimento.month, atleta.data_nascimento.day))
    
    # Formata a data de nascimento
    data_nascimento_formatada = atleta.data_nascimento.strftime('%d/%m/%Y')
    
    # Busca dados relacionados
    estatisticas = EstatisticaAtleta.objects.filter(atleta=atleta).first()
    certificados = CertificadoAtleta.objects.filter(atleta=atleta).order_by('-data_emissao')
    historico_competicoes = HistoricoCompeticao.objects.filter(atleta=atleta).order_by('-data_participacao')
    
    # Encontrar o logo
    logo_path = finders.find('competicoes/img/icone_keychart.png')
    logo_base64 = None
    if logo_path:
        try:
            with open(logo_path, "rb") as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
    
    # Informações adicionais
    info_adicional = {
        'academia_nome': atleta.academia.nome if atleta.academia else "Não informado",
        'graduacao': f"Faixa {atleta.get_faixa_display()}",
        'anos_experiencia': estatisticas.anos_experiencia if estatisticas else 0,
        'melhor_luta': estatisticas.melhor_luta if estatisticas else "Não registrado"
    }
    
    context = {
        'atleta': atleta,
        'idade': idade,
        'data_nascimento_formatada': data_nascimento_formatada,
        'estatisticas': estatisticas,
        'certificados': certificados,
        'historico_competicoes': historico_competicoes,
        'info_adicional': info_adicional,
        'logo_base64': logo_base64,
        'data_geracao': timezone.now()
    }
    
    # Configurar resposta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="perfil_{atleta.nome_completo.replace(" ", "_")}.pdf"'
    
    # Renderizar template
    template = get_template('atletas/perfil_atleta_pdf.html')
    html = template.render(context)
    
    # Gerar PDF
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    return response


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

    # Buscar ou criar estatísticas do atleta
    estatisticas, created = EstatisticaAtleta.objects.get_or_create(atleta=atleta)
    
    if created:
        # Se as estatísticas foram criadas agora, vamos populá-las com dados reais
        from app.competicoes.models import ResultadoKata, PartidaKumite
        
        # Contar resultados de kata
        resultados_kata = ResultadoKata.objects.filter(atleta=atleta)
        
        # Contar partidas de kumite
        partidas_kumite = PartidaKumite.objects.filter(
            models.Q(atleta1=atleta) | models.Q(atleta2=atleta)
        )
        
        # Atualizar estatísticas
        estatisticas.medalhas_ouro = resultados_kata.filter(posicao=1).count()
        estatisticas.medalhas_prata = resultados_kata.filter(posicao=2).count()
        estatisticas.medalhas_bronze = resultados_kata.filter(posicao=3).count()
        
        # Contar vitórias/derrotas em kumite
        vitorias = partidas_kumite.filter(vencedor=atleta).count()
        derrotas = partidas_kumite.exclude(vencedor=atleta).exclude(vencedor__isnull=True).count()
        empates = partidas_kumite.filter(vencedor__isnull=True).count()
        
        estatisticas.total_lutas = partidas_kumite.count()
        estatisticas.vitorias = vitorias
        estatisticas.derrotas = derrotas
        estatisticas.empates = empates
        
        # Melhor pontuação
        melhor_resultado = resultados_kata.order_by('-total').first()
        if melhor_resultado:
            estatisticas.melhor_pontuacao = melhor_resultado.total
            estatisticas.melhor_luta = f"Kata - {melhor_resultado.competicao.nome}"
        
        # Anos de experiência (estimado pela data de inscrição)
        anos_experiencia = hoje.year - atleta.data_inscricao.year
        estatisticas.anos_experiencia = max(1, anos_experiencia)
        
        estatisticas.save()
    
    # Buscar certificados do atleta
    certificados = CertificadoAtleta.objects.filter(atleta=atleta).order_by('-data_emissao')
    
    # Se não há certificados, criar alguns padrão
    if not certificados.exists():
        # Criar certificado de faixa
        CertificadoAtleta.objects.create(
            atleta=atleta,
            titulo=f"Faixa {atleta.get_faixa_display()}",
            tipo='graduacao',
            entidade_emissora="Federação Brasileira de Karatê",
            descricao=f"Certificado de graduação para faixa {atleta.get_faixa_display().lower()}",
            data_emissao=atleta.data_inscricao.date(),
            status='valido'
        )
        
        # Certificados baseados nas conquistas
        if estatisticas.medalhas_ouro > 0:
            CertificadoAtleta.objects.create(
                atleta=atleta,
                titulo="Campeão Nacional 2023",
                tipo='conquista',
                entidade_emissora="Confederação Brasileira de Karatê",
                descricao="Certificado de campeão nacional na categoria de karatê",
                data_emissao=hoje,
                status='valido'
            )
        
        # Atestado médico
        CertificadoAtleta.objects.create(
            atleta=atleta,
            titulo="Atestado Médico",
            tipo='medico',
            entidade_emissora="Clínica Esportiva",
            descricao="Atestado médico de aptidão para prática de karatê competitivo",
            data_emissao=hoje,
            data_validade=date(hoje.year + 1, hoje.month, hoje.day),
            status='expirando' if (date(hoje.year + 1, hoje.month, hoje.day) - hoje).days < 90 else 'valido'
        )
        
        # Recarregar certificados
        certificados = CertificadoAtleta.objects.filter(atleta=atleta).order_by('-data_emissao')
    
    # Buscar histórico de competições
    historico_competicoes = HistoricoCompeticao.objects.filter(atleta=atleta).order_by('-data_participacao')
    
    # Se não há histórico, criar alguns registros baseados nos resultados existentes
    if not historico_competicoes.exists():
        from app.competicoes.models import ResultadoKata
        
        resultados_existentes = ResultadoKata.objects.filter(atleta=atleta).select_related('competicao', 'categoria')
        
        for resultado in resultados_existentes:
            if resultado.posicao == 1:
                resultado_texto = '1º'
            elif resultado.posicao == 2:
                resultado_texto = '2º'
            elif resultado.posicao == 3:
                resultado_texto = '3º'
            else:
                resultado_texto = 'eliminado'
            
            HistoricoCompeticao.objects.get_or_create(
                atleta=atleta,
                competicao=resultado.competicao,
                categoria=resultado.categoria,
                defaults={
                    'resultado': resultado_texto,
                    'pontuacao': resultado.total,
                    'data_participacao': resultado.data_criacao.date(),
                }
            )
        
        # Se ainda não há histórico, criar alguns registros fictícios
        if not HistoricoCompeticao.objects.filter(atleta=atleta).exists():
            competicoes_exemplo = [
                {
                    'nome': 'Torneio Nacional 2023',
                    'data': date(2023, 5, 15),
                    'categoria': 'Kumite -70kg',
                    'resultado': '1º',
                    'pontuacao': 8.5
                },
                {
                    'nome': 'Copa Estadual 2023',
                    'data': date(2023, 3, 22),
                    'categoria': 'Kumite -70kg',
                    'resultado': '2º',
                    'pontuacao': 7.8
                },
                {
                    'nome': 'Campeonato Regional 2022',
                    'data': date(2022, 11, 10),
                    'categoria': 'Kumite -70kg',
                    'resultado': '1º',
                    'pontuacao': 8.2
                },
                {
                    'nome': 'Torneio Aberto 2022',
                    'data': date(2022, 8, 5),
                    'categoria': 'Kumite -70kg',
                    'resultado': 'eliminado',
                    'pontuacao': 6.5
                }
            ]
            
            for comp in competicoes_exemplo:
                HistoricoCompeticao.objects.create(
                    atleta=atleta,
                    competicao=atleta.competicao,  # Usa a competição atual do atleta
                    categoria=atleta.categoria,
                    resultado=comp['resultado'],
                    pontuacao=comp['pontuacao'],
                    data_participacao=comp['data'],
                    observacoes=f"Participação no {comp['nome']}"
                )
        
        # Recarregar histórico
        historico_competicoes = HistoricoCompeticao.objects.filter(atleta=atleta).order_by('-data_participacao')

    # Informações adicionais para a view
    info_adicional = {
        'academia_nome': atleta.academia.nome if atleta.academia else "Não informado",
        'graduacao': f"Faixa {atleta.get_faixa_display()}",
        'anos_experiencia': estatisticas.anos_experiencia,
        'melhor_luta': estatisticas.melhor_luta or "Não registrado"
    }

    # Prepara o contexto
    context = {
        'atleta': atleta,
        'idade': idade,
        'data_nascimento_formatada': data_nascimento_formatada,
        'estatisticas': estatisticas,
        'certificados': certificados[:4],  # Mostrar apenas os 4 primeiros
        'historico_competicoes': historico_competicoes[:4],  # Mostrar apenas os 4 primeiros
        'info_adicional': info_adicional,
    }

    return render(request, 'atletas/perfil_atleta.html', context)
