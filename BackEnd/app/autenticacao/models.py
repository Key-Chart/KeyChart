from django.db import models

'''class User(models.Model):
    nome = models.CharField(max_length=100, null=False)
    senha = models.CharField(max_length=100, null=False)
    lembrarDeMin = models.BooleanField()

    def __str__(self):
        return self.nome

class Contas(models.Model):
    nomeCompleto = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(max_length=150, null=False, unique=True)
    senha = models.CharField(max_length=100, null=False)
    confirmarSenha = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nomeCompleto'''