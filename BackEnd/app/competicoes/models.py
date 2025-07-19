from django.db import models
from django.utils import timezone

class Arbitro(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Árbitro'
        verbose_name_plural = 'Árbitros'

class Competicao(models.Model):
    STATUS_CHOICES = [
        ('Ativa', 'Ativa'),
        ('Finalizada', 'Finalizada'),
        ('Em breve', 'Em breve'),
    ]
    
    INSCRICOES_STATUS_CHOICES = [
        ('abertas', 'Abertas'),
        ('fechadas', 'Fechadas'),
        ('em-breve', 'Em breve'),
    ]

    # Informações básicas
    nome = models.CharField(max_length=100, null=False, blank=False)
    modalidade = models.CharField(max_length=50, null=False, blank=False)
    data_inicio = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=150, null=False, blank=False)
    regras_especificas = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Ativa'
    )
    
    # Árbitros (relacionamento Many-to-Many)
    arbitros = models.ManyToManyField(Arbitro, blank=True, related_name='competicoes')
    
    # Configurações de inscrições
    inscricoes_abertas = models.BooleanField(
        'Inscrições Abertas?',
        default=True,
        help_text="Marque se as inscrições estão abertas"
    )
    inscricoes_status = models.CharField(
        max_length=10,
        choices=INSCRICOES_STATUS_CHOICES,
        default='abertas'
    )
    inscricoes_data_limite = models.DateField(blank=True, null=True)
    inscricoes_valor = models.DecimalField(max_digits=10, decimal_places=2, default=120.00)
    inscricoes_taxa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    inscricoes_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Métodos de pagamento
    inscricoes_pagamento_pix = models.BooleanField(default=True)
    inscricoes_pagamento_cartao = models.BooleanField(default=True)
    inscricoes_pagamento_boleto = models.BooleanField(default=False)
    
    # Configurações de exibição
    inscricoes_mostrar_valor = models.BooleanField(default=True)
    inscricoes_mostrar_vagas = models.BooleanField(default=False)
    inscricoes_mensagem = models.TextField(blank=True, null=True)
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.data_inicio:
            return f"{self.nome} ({self.data_inicio.year})"
        return self.nome
    
    @property
    def valor_final_inscricao(self):
        """Calcula o valor final da inscrição (valor + taxa - desconto)"""
        return self.inscricoes_valor + self.inscricoes_taxa - self.inscricoes_desconto
    
    class Meta:
        verbose_name = 'Competição'
        verbose_name_plural = 'Competições'
        ordering = ['-data_inicio']

class Categoria(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('MX', 'Misto'),
    ]
    TIPO_CHOICES = [
        ('GI', 'Gi'),
        ('NOGI', 'No-Gi'),
        ('ABS', 'Absolute'),
    ]
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100, null=False, blank=False)
    sexo = models.CharField(max_length=2, choices=SEXO_CHOICES, null=False, blank=False)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, null=False, blank=False)

    def __str__(self):
        return f"{self.nome} - {self.get_sexo_display()} - {self.get_tipo_display()}"

class Academia(models.Model):
    competicao = models.ForeignKey('Competicao', on_delete=models.CASCADE, related_name='academias')
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # Sigla do estado (ex: SP, RJ)
    endereco = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.cidade}/{self.estado})"

class ResultadoKata(models.Model):
    FASE_CHOICES = [
        ('eliminatorias', 'Eliminatórias'),
        ('semifinal', 'Semifinal'),
        ('final', 'Final'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('classificado', 'Classificado'),
        ('eliminado', 'Eliminado'),
    ]

    atleta = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='resultados_kata')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    fase = models.CharField(max_length=20, choices=FASE_CHOICES, default='eliminatorias')
    nota1 = models.FloatField(default=0.0)
    nota2 = models.FloatField(default=0.0)
    nota3 = models.FloatField(default=0.0)
    nota4 = models.FloatField(default=0.0)
    nota5 = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    posicao = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    salvo = models.BooleanField(default=False)  # Indica se as notas já foram salvas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('atleta', 'categoria', 'fase')
        ordering = ['-total', 'posicao']

    def save(self, *args, **kwargs):
        notas = [self.nota1, self.nota2, self.nota3, self.nota4, self.nota5]
        # Remove a maior e menor nota (critério do karatê)
        if len([n for n in notas if n > 0]) >= 3:
            notas_ordenadas = sorted([n for n in notas if n > 0])
            if len(notas_ordenadas) >= 3:
                notas_validas = notas_ordenadas[1:-1]  # Remove menor e maior
                self.total = sum(notas_validas)
            else:
                self.total = sum(notas_ordenadas)
        else:
            self.total = sum(notas)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.atleta.nome_completo} - {self.fase} - {self.total}"


class ChaveamentoKata(models.Model):
    categoria = models.OneToOneField(Categoria, on_delete=models.CASCADE, related_name='chaveamento_kata')
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    fase_atual = models.CharField(
        max_length=20,
        choices=ResultadoKata.FASE_CHOICES,
        default='eliminatorias'
    )
    finalizado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Chaveamento Kata - {self.categoria.nome}"

    def get_resultados_fase(self, fase):
        """Retorna os resultados de uma fase específica"""
        return ResultadoKata.objects.filter(
            categoria=self.categoria,
            fase=fase
        ).order_by('-total')

    def avançar_fase(self):
        """Avança para a próxima fase do chaveamento"""
        if self.fase_atual == 'eliminatorias':
            self.fase_atual = 'semifinal'
        elif self.fase_atual == 'semifinal':
            self.fase_atual = 'final'
        elif self.fase_atual == 'final':
            self.finalizado = True
            self.data_finalizacao = timezone.now()
        self.save()

    def get_classificados_fase_anterior(self):
        """Retorna os atletas classificados da fase anterior"""
        fase_anterior = None
        if self.fase_atual == 'semifinal':
            fase_anterior = 'eliminatorias'
        elif self.fase_atual == 'final':
            fase_anterior = 'semifinal'
        
        if fase_anterior:
            return ResultadoKata.objects.filter(
                categoria=self.categoria,
                fase=fase_anterior,
                status='classificado'
            ).order_by('-total')
        return ResultadoKata.objects.none()

    def get_podio(self):
        """Retorna o pódio final"""
        if self.finalizado:
            return self.get_resultados_fase('final')[:3]
        return []

# Modelos para Kumitê
class ChaveamentoKumite(models.Model):
    TIPO_CHAVEAMENTO_CHOICES = [
        ('eliminacao_simples', 'Eliminação Simples'),
        ('eliminacao_dupla', 'Eliminação Dupla'),
        ('grupo_eliminacao', 'Grupos + Eliminação'),
    ]
    
    categoria = models.OneToOneField(Categoria, on_delete=models.CASCADE, related_name='chaveamento_kumite')
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    tipo_chaveamento = models.CharField(
        max_length=20,
        choices=TIPO_CHAVEAMENTO_CHOICES,
        default='eliminacao_simples'
    )
    fase_atual = models.CharField(max_length=50, default='oitavas')
    finalizado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Chaveamento Kumite - {self.categoria.nome}"

    def get_numero_atletas(self):
        """Retorna o número de atletas na categoria"""
        from app.atletas.models import Atleta
        return Atleta.objects.filter(categoria=self.categoria).count()

    def determinar_fases(self):
        """Determina as fases baseado no número de atletas"""
        num_atletas = self.get_numero_atletas()
        if num_atletas <= 2:
            return ['final']
        elif num_atletas <= 4:
            return ['semifinal', 'final']
        elif num_atletas <= 8:
            return ['quartas', 'semifinal', 'final']
        elif num_atletas <= 16:
            return ['oitavas', 'quartas', 'semifinal', 'final']
        else:
            return ['primeira_fase', 'oitavas', 'quartas', 'semifinal', 'final']

    def get_proximo_fase(self, fase_atual):
        """Retorna a próxima fase"""
        fases = self.determinar_fases()
        try:
            index_atual = fases.index(fase_atual)
            if index_atual < len(fases) - 1:
                return fases[index_atual + 1]
        except ValueError:
            pass
        return None


class PartidaKumite(models.Model):
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    RESULTADO_CHOICES = [
        ('vitoria_atleta1', 'Vitória Atleta 1'),
        ('vitoria_atleta2', 'Vitória Atleta 2'),
        ('empate', 'Empate'),
        ('wo_atleta1', 'WO Atleta 1'),
        ('wo_atleta2', 'WO Atleta 2'),
        ('desqualificacao_atleta1', 'Desqualificação Atleta 1'),
        ('desqualificacao_atleta2', 'Desqualificação Atleta 2'),
    ]

    chaveamento = models.ForeignKey(ChaveamentoKumite, on_delete=models.CASCADE, related_name='partidas')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    fase = models.CharField(max_length=50)
    round_numero = models.IntegerField(default=1)
    
    # Atletas
    atleta1 = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='partidas_kumite_atleta1', null=True, blank=True)
    atleta2 = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='partidas_kumite_atleta2', null=True, blank=True)
    
    # Resultado da partida
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada')
    resultado = models.CharField(max_length=30, choices=RESULTADO_CHOICES, null=True, blank=True)
    vencedor = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='vitorias_kumite', null=True, blank=True)
    
    # Pontuação detalhada
    pontos_atleta1 = models.IntegerField(default=0)
    pontos_atleta2 = models.IntegerField(default=0)
    
    # Advertências e punições
    advertencias_atleta1 = models.IntegerField(default=0)  # Chukoku
    advertencias_atleta2 = models.IntegerField(default=0)
    penalidades_atleta1 = models.IntegerField(default=0)   # Keikoku, Hansoku-chui, Hansoku
    penalidades_atleta2 = models.IntegerField(default=0)
    
    # Metadados
    tempo_luta = models.DurationField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chaveamento', 'fase', 'round_numero')
        ordering = ['fase', 'round_numero']

    def __str__(self):
        atleta1_nome = self.atleta1.nome_completo if self.atleta1 else "TBD"
        atleta2_nome = self.atleta2.nome_completo if self.atleta2 else "TBD"
        return f"{self.fase} - {atleta1_nome} vs {atleta2_nome}"

    def determinar_vencedor(self):
        """Determina o vencedor baseado nas regras do karatê"""
        if self.resultado in ['vitoria_atleta1', 'wo_atleta1', 'desqualificacao_atleta2']:
            self.vencedor = self.atleta1
        elif self.resultado in ['vitoria_atleta2', 'wo_atleta2', 'desqualificacao_atleta1']:
            self.vencedor = self.atleta2
        else:
            self.vencedor = None
        self.save()

    def get_status_display_custom(self):
        """Retorna o status formatado"""
        if self.status == 'finalizada':
            if self.vencedor:
                return f"Vencedor: {self.vencedor.nome_completo}"
            return "Empate"
        return self.get_status_display()


class PontuacaoKumite(models.Model):
    TIPO_PONTUACAO_CHOICES = [
        ('ippon', 'Ippon (3 pontos)'),
        ('waza_ari', 'Waza-ari (2 pontos)'),
        ('yuko', 'Yuko (1 ponto)'),
    ]
    
    TIPO_PENALIDADE_CHOICES = [
        ('chukoku', 'Chukoku (Advertência)'),
        ('keikoku', 'Keikoku (Penalidade)'),
        ('hansoku_chui', 'Hansoku-chui (Penalidade Grave)'),
        ('hansoku', 'Hansoku (Desqualificação)'),
    ]

    partida = models.ForeignKey(PartidaKumite, on_delete=models.CASCADE, related_name='pontuacoes')
    atleta = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_PONTUACAO_CHOICES + TIPO_PENALIDADE_CHOICES)
    pontos = models.IntegerField(default=0)
    tempo_acao = models.DurationField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']

    def __str__(self):
        return f"{self.atleta.nome_completo} - {self.get_tipo_display()} ({self.pontos})"