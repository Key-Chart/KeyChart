from django.db import models
from django.utils import timezone
import json


class EstatisticaCache(models.Model):
    """Modelo para cache de estatísticas para melhorar performance"""
    
    TIPOS_ESTATISTICA = [
        ('dashboard', 'Dashboard Principal'),
        ('atletas', 'Estatísticas de Atletas'),
        ('competicoes', 'Estatísticas de Competições'),
        ('academias', 'Estatísticas de Academias'),
        ('comparativas', 'Análises Comparativas'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPOS_ESTATISTICA)
    chave = models.CharField(max_length=100)  # Identificador único da estatística
    dados = models.JSONField()  # Dados em formato JSON
    parametros = models.JSONField(default=dict, blank=True)  # Parâmetros usados para gerar
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    expira_em = models.DateTimeField()  # Quando o cache expira
    ativo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'estatisticas_cache'
        unique_together = ['tipo', 'chave']
        indexes = [
            models.Index(fields=['tipo', 'chave']),
            models.Index(fields=['expira_em']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.chave}"
    
    @property
    def expirado(self):
        """Verifica se o cache está expirado"""
        return timezone.now() > self.expira_em
    
    def invalidar(self):
        """Marca o cache como inativo"""
        self.ativo = False
        self.save()


class AlertaEstatistica(models.Model):
    """Modelo para alertas baseados em estatísticas"""
    
    TIPOS_ALERTA = [
        ('info', 'Informativo'),
        ('warning', 'Aviso'),
        ('danger', 'Perigo'),
        ('success', 'Sucesso'),
    ]
    
    PRIORIDADES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPOS_ALERTA, default='info')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES, default='media')
    metrica_relacionada = models.CharField(max_length=100, blank=True)  # Métrica que gerou o alerta
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_esperado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acao_sugerida = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)
    data_visualizacao = models.DateTimeField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'estatisticas_alertas'
        ordering = ['-data_criacao', '-prioridade']
        indexes = [
            models.Index(fields=['tipo', 'ativo']),
            models.Index(fields=['prioridade', 'visualizado']),
        ]
    
    def __str__(self):
        return f"{self.titulo} ({self.get_prioridade_display()})"
    
    def marcar_como_visualizado(self):
        """Marca o alerta como visualizado"""
        self.visualizado = True
        self.data_visualizacao = timezone.now()
        self.save()


class MetricaPersonalizada(models.Model):
    """Modelo para métricas personalizadas definidas pelo usuário"""
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    consulta_sql = models.TextField()  # Query SQL para calcular a métrica
    formato_exibicao = models.CharField(max_length=50, default='numero')  # numero, percentual, moeda, etc.
    icone = models.CharField(max_length=50, default='bi-graph-up')
    cor = models.CharField(max_length=7, default='#3498db')  # Cor em hexadecimal
    ativa = models.BooleanField(default=True)
    ordem_exibicao = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'estatisticas_metricas_personalizadas'
        ordering = ['ordem_exibicao', 'nome']
    
    def __str__(self):
        return self.nome
