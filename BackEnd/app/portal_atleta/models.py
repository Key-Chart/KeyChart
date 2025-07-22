from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from app.inscricoes_online.models import InscricaoOnline
from app.atletas.models import Atleta
from app.competicoes.models import Competicao
import uuid

class AtletaUserManager(BaseUserManager):
    """
    Manager customizado para o modelo AtletaUser
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class AtletaUser(AbstractBaseUser):
    """
    Modelo de usuário específico para atletas
    Integra com as inscrições online para autenticação
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True)
    
    # Relacionamentos
    inscricao_origem = models.ForeignKey(
        InscricaoOnline, 
        on_delete=models.CASCADE, 
        related_name='atleta_user',
        help_text="Inscrição que originou este usuário"
    )
    
    # Status e controle
    is_active = models.BooleanField(default=True)
    email_verificado = models.BooleanField(default=False)
    primeiro_acesso = models.BooleanField(default=True)
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ultimo_acesso = models.DateTimeField(blank=True, null=True)
    
    objects = AtletaUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']
    
    class Meta:
        verbose_name = "Usuário Atleta"
        verbose_name_plural = "Usuários Atletas"
        db_table = 'portal_atleta_user'
    
    def __str__(self):
        return f"{self.nome_completo} ({self.email})"
    
    def get_inscricoes(self):
        """Retorna todas as inscrições do atleta"""
        return InscricaoOnline.objects.filter(email=self.email)
    
    def get_competicoes(self):
        """Retorna todas as competições do atleta"""
        return Competicao.objects.filter(
            inscricoes_online__email=self.email
        ).distinct()
    
    def marcar_primeiro_acesso(self):
        """Marca que o atleta já fez o primeiro acesso"""
        if self.primeiro_acesso:
            self.primeiro_acesso = False
            self.save()

class SessaoAtleta(models.Model):
    """
    Modelo para gerenciar sessões de atletas
    """
    atleta = models.ForeignKey(AtletaUser, on_delete=models.CASCADE, related_name='sessoes')
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_ultima_atividade = models.DateTimeField(auto_now=True)
    ativa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sessão de Atleta"
        verbose_name_plural = "Sessões de Atletas"
        db_table = 'portal_atleta_sessao'
    
    def __str__(self):
        return f"Sessão de {self.atleta.nome_completo} - {self.data_inicio}"

class NotificacaoAtleta(models.Model):
    """
    Sistema de notificações para atletas
    """
    TIPO_CHOICES = [
        ('inscricao', 'Inscrição'),
        ('pagamento', 'Pagamento'),
        ('competicao', 'Competição'),
        ('resultado', 'Resultado'),
        ('sistema', 'Sistema'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    atleta = models.ForeignKey(AtletaUser, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='normal')
    
    # Status
    lida = models.BooleanField(default=False)
    data_leitura = models.DateTimeField(blank=True, null=True)
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True)
    expirar_em = models.DateTimeField(blank=True, null=True)
    
    # Links e ações
    link_acao = models.URLField(blank=True, help_text="Link para ação relacionada")
    dados_extras = models.JSONField(blank=True, null=True, help_text="Dados adicionais da notificação")
    
    class Meta:
        verbose_name = "Notificação de Atleta"
        verbose_name_plural = "Notificações de Atletas"
        db_table = 'portal_atleta_notificacao'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.atleta.nome_completo}"
    
    def marcar_como_lida(self):
        """Marca notificação como lida"""
        if not self.lida:
            self.lida = True
            self.data_leitura = timezone.now()
            self.save()

class PreferenciaAtleta(models.Model):
    """
    Preferências e configurações do atleta
    """
    atleta = models.OneToOneField(AtletaUser, on_delete=models.CASCADE, related_name='preferencias')
    
    # Notificações
    receber_email_inscricao = models.BooleanField(default=True)
    receber_email_pagamento = models.BooleanField(default=True)
    receber_email_competicao = models.BooleanField(default=True)
    receber_email_resultado = models.BooleanField(default=True)
    
    # Privacidade
    perfil_publico = models.BooleanField(default=False)
    mostrar_resultados = models.BooleanField(default=True)
    mostrar_estatisticas = models.BooleanField(default=True)
    
    # Interface
    tema_escuro = models.BooleanField(default=False)
    idioma = models.CharField(max_length=10, default='pt-br')
    
    # Dados adicionais
    configuracoes_extras = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Preferência de Atleta"
        verbose_name_plural = "Preferências de Atletas"
        db_table = 'portal_atleta_preferencia'
    
    def __str__(self):
        return f"Preferências - {self.atleta.nome_completo}"

class LogAtividadeAtleta(models.Model):
    """
    Log de atividades do atleta no portal
    """
    ACAO_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('visualizacao', 'Visualização'),
        ('download', 'Download'),
        ('alteracao', 'Alteração'),
        ('inscricao', 'Inscrição'),
        ('pagamento', 'Pagamento'),
    ]
    
    atleta = models.ForeignKey(AtletaUser, on_delete=models.CASCADE, related_name='logs')
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    descricao = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    dados_extras = models.JSONField(blank=True, null=True)
    data_acao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Log de Atividade"
        verbose_name_plural = "Logs de Atividades"
        db_table = 'portal_atleta_log'
        ordering = ['-data_acao']
    
    def __str__(self):
        return f"{self.acao} - {self.atleta.nome_completo} - {self.data_acao}"
