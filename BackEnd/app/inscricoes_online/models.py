from django.db import models
from django.utils import timezone
from app.competicoes.models import Competicao, Categoria
from app.atletas.models import Academia
import uuid
import secrets
import string

class InscricaoOnline(models.Model):
    """
    Modelo para gerenciar inscrições online públicas
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente de Pagamento'),
        ('pago', 'Pagamento Confirmado'),
        ('confirmado', 'Inscrição Confirmada'),
        ('cancelado', 'Cancelado'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
    ]
    
    # Identificação única
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    numero_inscricao = models.CharField(max_length=20, unique=True, blank=True)
    
    # Dados da competição
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name='inscricoes_online')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    # Dados pessoais do atleta
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    
    # Dados do karatê
    faixa = models.CharField(max_length=10, choices=[
        ('branca', 'Branca'),
        ('azul', 'Azul'),
        ('amarela', 'Amarela'),
        ('laranja', 'Laranja'),
        ('verde', 'Verde'),
        ('roxa', 'Roxa'),
        ('marrom', 'Marrom'),
        ('preta', 'Preta'),
    ])
    
    # Dados físicos
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.IntegerField()  # em cm
    
    # Localização
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    
    # Academia
    academia_nome = models.CharField(max_length=100)
    academia_cidade = models.CharField(max_length=50)
    academia_estado = models.CharField(max_length=2)
    academia = models.ForeignKey(Academia, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Foto
    foto = models.ImageField(upload_to='inscricoes_online/', null=True, blank=True)
    
    # Status e pagamento
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    forma_pagamento = models.CharField(max_length=10, choices=FORMA_PAGAMENTO_CHOICES, blank=True)
    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Credenciais do atleta (para futuro painel)
    senha_atleta = models.CharField(max_length=20, blank=True)
    senha_enviada = models.BooleanField(default=False)
    
    # Dados de pagamento - comentados para futuro uso com Mercado Pago
    # payment_id = models.CharField(max_length=100, blank=True, null=True)
    # preference_id = models.CharField(max_length=100, blank=True, null=True)
    # payment_status = models.CharField(max_length=50, blank=True, null=True)
    
    # Metadados
    data_inscricao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ip_inscricao = models.GenericIPAddressField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_inscricao:
            # Gera número único da inscrição
            ano = timezone.now().year
            count = InscricaoOnline.objects.filter(
                competicao=self.competicao,
                data_inscricao__year=ano
            ).count() + 1
            self.numero_inscricao = f"{self.competicao.id}{ano}{count:04d}"
        
        if not self.senha_atleta:
            # Gera senha aleatória para o atleta
            self.senha_atleta = self.gerar_senha_aleatoria()
        
        if not self.valor_inscricao and self.competicao:
            # Define valor da inscrição baseado na competição
            self.valor_inscricao = self.competicao.valor_final_inscricao
        
        super().save(*args, **kwargs)
    
    def gerar_senha_aleatoria(self, length=8):
        """Gera uma senha aleatória para o atleta"""
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def get_idade(self):
        """Calcula a idade do atleta"""
        today = timezone.now().date()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    
    def __str__(self):
        return f"{self.nome_completo} - {self.competicao.nome}"
    
    class Meta:
        verbose_name = 'Inscrição Online'
        verbose_name_plural = 'Inscrições Online'
        ordering = ['-data_inscricao']
        unique_together = ['competicao', 'email']  # Evita inscrições duplicadas


class LogInscricao(models.Model):
    """
    Log de ações realizadas na inscrição
    """
    inscricao = models.ForeignKey(InscricaoOnline, on_delete=models.CASCADE, related_name='logs')
    acao = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.inscricao.nome_completo} - {self.acao}"
    
    class Meta:
        ordering = ['-data']
