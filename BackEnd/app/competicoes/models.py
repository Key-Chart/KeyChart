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
        default=False,
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

class Atleta(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    FAIXA_CHOICES = [
        ('BRANCA', 'Branca'),
        ('AZUL', 'Azul'),
        ('ROXA', 'Roxa'),
        ('MARROM', 'Marrom'),
        ('PRETA', 'Preta'),
    ]
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='atletas')
    academia = models.ForeignKey(Academia, on_delete=models.SET_NULL, null=True, blank=True)
    nome_completo = models.CharField(max_length=200, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=False, blank=False)
    idade = models.PositiveIntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
    altura = models.DecimalField(max_digits=3, decimal_places=2)  # in meters
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=20)
    faixa = models.CharField(max_length=10, choices=FAIXA_CHOICES, null=False, blank=False)
    cidade = models.CharField(max_length=100, null=False, blank=False)
    estado = models.CharField(max_length=2, null=False, blank=False)
    foto = models.ImageField(upload_to='atletas/', null=True, blank=True)

    def __str__(self):
        return self.nome_completo