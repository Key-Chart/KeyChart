from django.db import models

class Competicao(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    modalidade = models.CharField(max_length=50, null=False, blank=False)
    data_inicio = models.DateTimeField()
    horario = models.CharField()
    local = models.CharField(max_length=150, null=False, blank=False)
    arbitros = models.TextField(blank=True, null=True)
    regras_especificas = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Ativa')

    def __str__(self):
        return self.nome