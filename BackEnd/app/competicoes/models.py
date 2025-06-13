from django.db import models

class Competicao(models.Model):
    STATUS_CHOICES = [
        ('Ativa', 'Ativa'),
        ('Cancelada', 'Cancelada'),
        ('Concluída', 'Concluída'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Ativa'
    )
    inscricoes_abertas = models.BooleanField(
        'Inscrições Abertas?',
        default=True,
        help_text="Marque se as inscrições estão abertas"
    )
    nome = models.CharField(max_length=100, null=False, blank=False)
    modalidade = models.CharField(max_length=50, null=False, blank=False)
    data_inicio = models.DateTimeField()
    horario = models.CharField(max_length=50, null=False, blank=False)
    local = models.CharField(max_length=150, null=False, blank=False)
    arbitros = models.TextField(blank=True, null=True)
    regras_especificas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.data_inicio.year})"

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
    atleta = models.ForeignKey('atletas.Atleta', on_delete=models.CASCADE, related_name='resultados_kata')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    nota1 = models.FloatField()
    nota2 = models.FloatField()
    nota3 = models.FloatField()
    nota4 = models.FloatField()
    nota5 = models.FloatField()
    total = models.FloatField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('atleta', 'categoria')  # Garante apenas um resultado por atleta por categoria

    def save(self, *args, **kwargs):
        notas = [self.nota1, self.nota2, self.nota3, self.nota4, self.nota5]

        # Remove a maior e menor nota apenas se houver pelo menos 3 notas
        if len([n for n in notas if n is not None]) >= 3:
            notas_validas = sorted(notas)[1:-1]  # Remove a menor e a maior
            self.total = sum(notas_validas) / len(notas_validas)  # Média das restantes
        else:
            self.total = sum(notas) / len([n for n in notas if n is not None])

        super().save(*args, **kwargs)