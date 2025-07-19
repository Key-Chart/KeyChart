from django.db import models
from app.competicoes.models import Competicao, Categoria, Academia

class Atleta(models.Model):
    FAIXA_CHOICES = [
        ('branca', 'Branca'),
        ('azul', 'Azul'),
        ('amarela', 'Amarela'),
        ('laranja', 'Laranja'),
        ('verde', 'Verde'),
        ('roxa', 'Roxa'),
        ('marrom', 'Marrom'),
        ('preta', 'Preta'),
    ]

    ESTADO_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('X', 'Misto'),
    ]

    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name='atletas')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    academia = models.ForeignKey(Academia, on_delete=models.SET_NULL, null=True, blank=True)

    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    idade = models.IntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.IntegerField(default=0, null=False, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True, verbose_name='CPF')
    rg = models.CharField(max_length=20, null=True, blank=True, verbose_name='RG')
    faixa = models.CharField(max_length=10, choices=FAIXA_CHOICES)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    foto = models.ImageField(upload_to='fotos_atletas/', null=True, blank=True)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.competicao.nome}"

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'
        ordering = ['nome_completo']

    def foto_url(self):
        return self.foto.url if self.foto else ''


class CertificadoAtleta(models.Model):
    STATUS_CHOICES = [
        ('valido', 'Válido'),
        ('expirando', 'Expirando'),
        ('expirado', 'Expirado'),
        ('suspenso', 'Suspenso'),
    ]

    TIPO_CHOICES = [
        ('graduacao', 'Graduação/Faixa'),
        ('conquista', 'Conquista/Campeonato'),
        ('medico', 'Atestado Médico'),
        ('curso', 'Curso/Capacitação'),
        ('arbitragem', 'Arbitragem'),
        ('outros', 'Outros'),
    ]

    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE, related_name='certificados')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outros')
    entidade_emissora = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_emissao = models.DateField()
    data_validade = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='valido')
    arquivo = models.FileField(upload_to='certificados/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.atleta.nome_completo}"

    class Meta:
        verbose_name = 'Certificado do Atleta'
        verbose_name_plural = 'Certificados dos Atletas'
        ordering = ['-data_emissao']


class EstatisticaAtleta(models.Model):
    atleta = models.OneToOneField(Atleta, on_delete=models.CASCADE, related_name='estatisticas')
    
    # Estatísticas gerais
    total_lutas = models.IntegerField(default=0)
    vitorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    
    # Estatísticas específicas do karatê
    ippon_aplicados = models.IntegerField(default=0)
    waza_ari_aplicados = models.IntegerField(default=0)
    yuko_aplicados = models.IntegerField(default=0)
    
    # Medalhas e conquistas
    medalhas_ouro = models.IntegerField(default=0)
    medalhas_prata = models.IntegerField(default=0)
    medalhas_bronze = models.IntegerField(default=0)
    
    # Melhor resultado
    melhor_luta = models.CharField(max_length=200, blank=True, null=True)
    melhor_pontuacao = models.FloatField(default=0.0)
    
    # Anos de experiência
    anos_experiencia = models.IntegerField(default=0)
    
    # Última atualização
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estatísticas - {self.atleta.nome_completo}"

    @property
    def taxa_vitoria(self):
        if self.total_lutas > 0:
            return round((self.vitorias / self.total_lutas) * 100, 1)
        return 0

    @property
    def total_medalhas(self):
        return self.medalhas_ouro + self.medalhas_prata + self.medalhas_bronze

    class Meta:
        verbose_name = 'Estatística do Atleta'
        verbose_name_plural = 'Estatísticas dos Atletas'


class HistoricoCompeticao(models.Model):
    RESULTADO_CHOICES = [
        ('1º', '1º Lugar'),
        ('2º', '2º Lugar'),
        ('3º', '3º Lugar'),
        ('eliminado', 'Eliminado'),
        ('desclassificado', 'Desclassificado'),
        ('nao_participou', 'Não Participou'),
    ]

    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE, related_name='historico_competicoes')
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    pontuacao = models.FloatField(default=0.0)
    observacoes = models.TextField(blank=True, null=True)
    data_participacao = models.DateField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.atleta.nome_completo} - {self.competicao.nome} ({self.resultado})"

    class Meta:
        verbose_name = 'Histórico de Competição'
        verbose_name_plural = 'Históricos de Competições'
        ordering = ['-data_participacao']
        unique_together = ('atleta', 'competicao', 'categoria')