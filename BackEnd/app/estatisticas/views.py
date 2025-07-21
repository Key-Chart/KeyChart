from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
import json

# ===============================
# VIEWS DE PÁGINAS
# ===============================

def dashboard_view(request):
    """Dashboard principal de estatísticas"""
    # Dados temporários de teste
    context = {
        'metricas_principais': {
            'total_atletas': 150,
            'total_competicoes': 25,
            'competicoes_mes': 5,
            'atletas_ativos': 140
        },
        'distribuicao_categoria': [],
        'distribuicao_sexo': {'masculino': 80, 'feminino': 70},
        'top_academias': [],
        'evolucao_inscricoes': [],
        'alertas': [],
        'cache_status': {'status': 'ativo'},
        'ultima_atualizacao': timezone.now()
    }
    
    return render(request, 'estatisticas/dashboard.html', context)


def competicoes_stats_view(request):
    """Página de estatísticas de competições"""
    context = {
        'total_competicoes': 25,
        'competicoes_mes': 5,
        'media_atletas': 6.8,
        'taxa_finalizacao': 85.5,
        'distribuicao_modalidade': [],
        'evolucao_competicoes': [],
    }
    
    return render(request, 'estatisticas/competicoes.html', context)


def atletas_stats_view(request):
    """Página de estatísticas de atletas"""
    context = {
        'total_atletas': 150,
        'atletas_ativos': 140,
        'crescimento_mensal': 12.5,
        'distribuicao_faixa': [],
        'distribuicao_estado': [],
        'distribuicao_sexo': {'masculino': 80, 'feminino': 70},
        'top_academias': [],
    }
    
    return render(request, 'estatisticas/atletas.html', context)


def academias_stats_view(request):
    """Página de estatísticas de academias"""
    context = {
        'top_academias': [],
        'distribuicao_estados': [],
        'media_atletas_academia': 8.2,
    }
    
    return render(request, 'estatisticas/academias.html', context)


def comparativas_view(request):
    """Página de análises comparativas"""
    context = {
        'evolucao_inscricoes': [],
        'comparativo_categorias': [],
        'comparativo_sexo': {'masculino': 80, 'feminino': 70},
        'tendencias': {
            'crescimento_atletas': 12.5,
            'tendencia_participacao': 8.3,
        }
    }
    
    return render(request, 'estatisticas/comparativas.html', context)


# ===============================
# VIEWS DE API (AJAX)
# ===============================

class MetricasAPIView(View):
    """API para métricas do dashboard"""
    
    def get(self, request):
        try:
            periodo = request.GET.get('periodo', '7d')
            
            metricas = {
                'total_atletas': 150,
                'total_competicoes': 25,
                'competicoes_mes': 5,
                'atletas_ativos': 140,
                'crescimento_atletas': 12.5,
                'tendencia_participacao': 8.3,
                'taxa_finalizacao': 85.5,
                'media_atletas_competicao': 6.8,
                'ultima_atualizacao': timezone.now().isoformat()
            }
            
            return JsonResponse({
                'success': True,
                'metricas': metricas,
                'periodo': periodo,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class GraficosAPIView(View):
    """API para dados de gráficos"""
    
    def get(self, request):
        try:
            periodo = request.GET.get('periodo', '7d')
            
            graficos_data = {
                'competicoes': {
                    'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                    'values': [12, 19, 8, 15, 25, 18]
                },
                'atletas': {
                    'labels': ['Branca', 'Azul', 'Roxa', 'Marrom', 'Preta'],
                    'values': [35, 25, 20, 15, 5]
                },
                'performance': {
                    'labels': ['Kata', 'Kumite', 'Equipes'],
                    'values': [85, 78, 92]
                }
            }
            
            return JsonResponse({
                'success': True,
                'graficos': graficos_data,
                'periodo': periodo
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class KPIsAPIView(View):
    """API para KPIs"""
    
    def get(self, request):
        try:
            kpis = {
                'participacao': {
                    'valor': 87.5,
                    'formato': 'percentage',
                    'meta': '85%'
                },
                'satisfacao': {
                    'valor': 4.2,
                    'formato': 'decimal',
                    'meta': '4.0'
                },
                'crescimento': {
                    'valor': 12.5,
                    'formato': 'percentage',
                    'meta': '10%'
                },
                'retencao': {
                    'valor': 92.3,
                    'formato': 'percentage',
                    'meta': '90%'
                }
            }
            
            return JsonResponse({
                'success': True,
                'kpis': kpis
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


def alertas_api_view(request):
    """API para alertas"""
    try:
        alertas = [
            {
                'tipo': 'info',
                'titulo': 'Sistema Funcionando',
                'mensagem': 'Todas as estatísticas estão sendo calculadas normalmente.',
                'created_at': timezone.now().isoformat()
            }
        ]
        
        return JsonResponse({
            'success': True,
            'alertas': alertas,
            'total': len(alertas)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def export_api_view(request):
    """API para exportação de dados"""
    try:
        formato = request.POST.get('formato', 'excel')
        periodo = request.POST.get('periodo', '7d')
        
        # Simular exportação
        return JsonResponse({
            'success': True,
            'message': f'Dados exportados em formato {formato}',
            'download_url': '/estatisticas/download/relatorio.xlsx'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
