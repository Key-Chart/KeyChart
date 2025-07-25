from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CodigoVerificacao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='codigo_verificacao')
    codigo = models.CharField(max_length=6)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Código para {self.user.email}: {self.codigo}"
