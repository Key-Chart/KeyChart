"""
Utilitários para cálculos de estatísticas - KeyChart
Sistema completo de análises e alertas
"""
from django.utils import timezone
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class EstatisticasCalculator:
    """
    Calculadora principal de estatísticas do sistema KeyChart
    Implementa todos os KPIs e métricas operacionais
    """
    
    def __init__(self):
        self.periodo_padrao = timedelta(days=30)
    
    # === MÉTRICAS DE ATLETAS ===
    
    def get_atletas_ativos(self, periodo_dias=30):
        """Retorna número de atletas ativos no período"""
        try:
            # TODO: Implementar quando modelos estiverem estáveis
            return 150  # Mock data
        except Exception as e:
            logger.error(f"Erro ao calcular atletas ativos: {e}")
            return 0
    
    def get_total_atletas(self):
        """Total de atletas cadastrados"""
        try:
            # TODO: Implementar quando modelos estiverem estáveis
            return 150  # Mock data
        except Exception as e:
            logger.error(f"Erro ao calcular total de atletas: {e}")
            return 0
    
    def get_crescimento_mensal_atletas(self):
        """Calcula taxa de crescimento mensal de atletas"""
        try:
            # TODO: Implementar cálculo real
            return 12.5  # Mock: 12.5% de crescimento
        except Exception as e:
            logger.error(f"Erro ao calcular crescimento mensal: {e}")
            return 0
    
    def get_distribuicao_faixas(self):
        """Retorna distribuição de atletas por faixa"""
        try:
            # TODO: Implementar quando modelo Atleta estiver estável
            return [
                {'faixa': 'Branca', 'total': 45},
                {'faixa': 'Azul', 'total': 35},
                {'faixa': 'Roxa', 'total': 25},
                {'faixa': 'Marrom', 'total': 15},
                {'faixa': 'Preta', 'total': 8}
            ]
        except Exception as e:
            logger.error(f"Erro ao calcular distribuição de faixas: {e}")
            return []
    
    def get_distribuicao_genero(self):
        """Retorna distribuição por gênero"""
        try:
            # TODO: Implementar
            return {'masculino': 80, 'feminino': 70}
        except Exception as e:
            logger.error(f"Erro ao calcular distribuição de gênero: {e}")
            return {'masculino': 0, 'feminino': 0}
    
    # === MÉTRICAS DE COMPETIÇÕES ===
    
    def get_competicoes_mes_atual(self):
        """Retorna número de competições do mês atual"""
        try:
            # TODO: Implementar
            return 5  # Mock data
        except Exception as e:
            logger.error(f"Erro ao calcular competições do mês: {e}")
            return 0
    
    def get_total_competicoes(self):
        """Total de competições"""
        try:
            # TODO: Implementar
            return 25  # Mock data
        except Exception as e:
            logger.error(f"Erro ao calcular total de competições: {e}")
            return 0
    
    def get_participacao_media(self):
        """Calcula participação média por competição"""
        try:
            # TODO: Implementar cálculo real
            return 8.5  # Mock: média de 8.5 atletas por competição
        except Exception as e:
            logger.error(f"Erro ao calcular participação média: {e}")
            return 0
    
    def get_taxa_finalizacao(self):
        """Taxa de competições finalizadas vs iniciadas"""
        try:
            # TODO: Implementar
            return 87.5  # Mock: 87.5% de finalização
        except Exception as e:
            logger.error(f"Erro ao calcular taxa de finalização: {e}")
            return 0
    
    # === MÉTRICAS DE PERFORMANCE ===
    
    def get_tempo_medio_organizacao(self):
        """Tempo médio para organizar uma competição"""
        try:
            # TODO: Implementar cálculo baseado em timestamps
            return 2.5  # Mock: 2.5 dias em média
        except Exception as e:
            logger.error(f"Erro ao calcular tempo de organização: {e}")
            return 0
    
    def get_eficiencia_chaveamento(self):
        """Eficiência do sistema de chaveamento"""
        try:
            # TODO: Implementar baseado em métricas de conflitos/reajustes
            return 94.2  # Mock: 94.2% de eficiência
        except Exception as e:
            logger.error(f"Erro ao calcular eficiência de chaveamento: {e}")
            return 0
    
    # === ANÁLISES TEMPORAIS ===
    
    def get_evolucao_inscricoes(self, periodo_dias=90):
        """Evolução de inscrições ao longo do tempo"""
        try:
            # TODO: Implementar série temporal
            return {
                'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                'values': [45, 52, 48, 61, 55, 67]
            }
        except Exception as e:
            logger.error(f"Erro ao calcular evolução de inscrições: {e}")
            return {'labels': [], 'values': []}
    
    def get_tendencia_participacao(self):
        """Calcula tendência de participação (crescimento/declínio)"""
        try:
            # TODO: Implementar cálculo de tendência
            return 8.3  # Mock: 8.3% de crescimento na tendência
        except Exception as e:
            logger.error(f"Erro ao calcular tendência de participação: {e}")
            return 0


class AlertasManager:
    """
    Sistema de alertas e notificações inteligentes
    Monitora KPIs e gera alertas automáticos
    """
    
    def __init__(self):
        self.calc = EstatisticasCalculator()
        self.thresholds = {
            'participacao_minima': 10,      # Mínimo de atletas por competição
            'crescimento_minimo': 5,        # % mínimo de crescimento mensal
            'taxa_finalizacao_minima': 80,  # % mínima de finalização
            'tempo_organizacao_maximo': 5,  # Dias máximos para organizar
        }
    
    def verificar_alertas(self):
        """
        Verifica todos os alertas possíveis e retorna lista de notificações
        """
        alertas = []
        
        try:
            # Alerta: Baixa participação
            participacao = self.calc.get_participacao_media()
            if participacao < self.thresholds['participacao_minima']:
                alertas.append({
                    'tipo': 'warning',
                    'titulo': 'Baixa Participação',
                    'mensagem': f'Média de apenas {participacao:.1f} atletas por competição',
                    'acao': 'revisar_estrategias_marketing',
                    'prioridade': 'alta',
                    'timestamp': timezone.now().isoformat()
                })
            
            # Alerta: Crescimento abaixo da meta
            crescimento = self.calc.get_crescimento_mensal_atletas()
            if crescimento < self.thresholds['crescimento_minimo']:
                alertas.append({
                    'tipo': 'info',
                    'titulo': 'Meta de Crescimento',
                    'mensagem': f'Crescimento de {crescimento:.1f}% abaixo da meta de {self.thresholds["crescimento_minimo"]}%',
                    'acao': 'implementar_campanhas',
                    'prioridade': 'media',
                    'timestamp': timezone.now().isoformat()
                })
            
            # Alerta: Taxa de finalização baixa
            taxa_finalizacao = self.calc.get_taxa_finalizacao()
            if taxa_finalizacao < self.thresholds['taxa_finalizacao_minima']:
                alertas.append({
                    'tipo': 'danger',
                    'titulo': 'Taxa de Finalização Baixa',
                    'mensagem': f'Apenas {taxa_finalizacao:.1f}% das competições são finalizadas',
                    'acao': 'revisar_processos',
                    'prioridade': 'alta',
                    'timestamp': timezone.now().isoformat()
                })
            
            # Alerta: Tempo de organização alto
            tempo_org = self.calc.get_tempo_medio_organizacao()
            if tempo_org > self.thresholds['tempo_organizacao_maximo']:
                alertas.append({
                    'tipo': 'warning',
                    'titulo': 'Tempo de Organização Alto',
                    'mensagem': f'Média de {tempo_org:.1f} dias para organizar competições',
                    'acao': 'otimizar_processos',
                    'prioridade': 'media',
                    'timestamp': timezone.now().isoformat()
                })
            
            # Alerta positivo: Sistema funcionando bem
            if not alertas:
                alertas.append({
                    'tipo': 'success',
                    'titulo': 'Sistema Operacional',
                    'mensagem': 'Todos os indicadores estão dentro dos parâmetros esperados',
                    'acao': 'manter_qualidade',
                    'prioridade': 'baixa',
                    'timestamp': timezone.now().isoformat()
                })
            
        except Exception as e:
            logger.error(f"Erro ao verificar alertas: {e}")
            alertas.append({
                'tipo': 'danger',
                'titulo': 'Erro no Sistema de Alertas',
                'mensagem': 'Não foi possível verificar todos os indicadores',
                'acao': 'verificar_sistema',
                'prioridade': 'alta',
                'timestamp': timezone.now().isoformat()
            })
        
        return alertas
    
    def get_alertas_por_prioridade(self, prioridade='alta'):
        """Filtra alertas por prioridade"""
        todos_alertas = self.verificar_alertas()
        return [alerta for alerta in todos_alertas if alerta['prioridade'] == prioridade]
    
    def criar_alerta_customizado(self, titulo, mensagem, tipo='info'):
        """Cria um alerta personalizado"""
        return {
            'tipo': tipo,
            'titulo': titulo,
            'mensagem': mensagem,
            'acao': 'acao_personalizada',
            'prioridade': 'media',
            'timestamp': timezone.now().isoformat(),
            'customizado': True
        }


class KPIsManager:
    """
    Gerenciador de KPIs (Key Performance Indicators)
    Calcula e monitora indicadores chave de performance
    """
    
    def __init__(self):
        self.calc = EstatisticasCalculator()
    
    def get_kpis_operacionais(self):
        """KPIs operacionais do sistema"""
        return {
            'atletas_ativos': {
                'valor': self.calc.get_atletas_ativos(),
                'formato': 'numero',
                'meta': 200,
                'tendencia': 'crescente'
            },
            'competicoes_mes': {
                'valor': self.calc.get_competicoes_mes_atual(),
                'formato': 'numero',
                'meta': 8,
                'tendencia': 'estavel'
            },
            'taxa_crescimento': {
                'valor': self.calc.get_crescimento_mensal_atletas(),
                'formato': 'percentage',
                'meta': 10.0,
                'tendencia': 'crescente'
            },
            'participacao_media': {
                'valor': self.calc.get_participacao_media(),
                'formato': 'decimal',
                'meta': 10.0,
                'tendencia': 'crescente'
            }
        }
    
    def get_kpis_qualidade(self):
        """KPIs de qualidade do serviço"""
        return {
            'taxa_finalizacao': {
                'valor': self.calc.get_taxa_finalizacao(),
                'formato': 'percentage',
                'meta': 90.0,
                'tendencia': 'estavel'
            },
            'eficiencia_chaveamento': {
                'valor': self.calc.get_eficiencia_chaveamento(),
                'formato': 'percentage',
                'meta': 95.0,
                'tendencia': 'crescente'
            },
            'tempo_organizacao': {
                'valor': self.calc.get_tempo_medio_organizacao(),
                'formato': 'dias',
                'meta': 3.0,
                'tendencia': 'decrescente'  # Queremos menos tempo
            },
            'satisfacao_usuarios': {
                'valor': 4.2,  # Mock data
                'formato': 'rating',
                'meta': 4.0,
                'tendencia': 'crescente'
            }
        }
    
    def get_todos_kpis(self):
        """Retorna todos os KPIs organizados por categoria"""
        return {
            'operacionais': self.get_kpis_operacionais(),
            'qualidade': self.get_kpis_qualidade(),
            'timestamp': timezone.now().isoformat()
        }
