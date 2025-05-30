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
    faixa = models.CharField(max_length=10, choices=FAIXA_CHOICES)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    foto = models.ImageField(upload_to='atletas/fotos/', null=True, blank=True)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_completo} - {self.competicao.nome}"

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'
        ordering = ['nome_completo']