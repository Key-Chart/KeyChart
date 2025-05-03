from django.db import models

class Competicao(models.Model):
    STATUS_CHOICES = [
        ('Ativa', 'Ativa'),
        ('Finalizada', 'Finalizada'),
        ('Em breve', 'Em breve'),
    ]
    
    nome = models.CharField(max_length=100)
    modalidade = models.CharField(max_length=50)
    data_inicio = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=150)
    arbitros = models.TextField(blank=True, null=True)
    regras_especificas = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    CATEGORIA_CHOICES = [
        ('Adulto', 'Adulto'),
        ('Infantil', 'Infantil'),
        ('Sênior', 'Sênior'),
    ]
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    ]
    TIPO_CHOICES = [
        ('Kata', 'Kata'),
        ('Kumitê', 'Kumitê'),
    ]

    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.categoria} - {self.sexo} - {self.tipo}"

class Academia(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    endereco = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome

class Atleta(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    ]

    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    idade = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    faixa = models.CharField(max_length=30, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    academia = models.ForeignKey(Academia, on_delete=models.SET_NULL, null=True)
    foto_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_completo

class Inscricao(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    ]

    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
    status_inscricao = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')

    class Meta:
        unique_together = ('atleta', 'categoria', 'competicao')

    def __str__(self):
        return f"{self.atleta} - {self.categoria} - {self.competicao}"
