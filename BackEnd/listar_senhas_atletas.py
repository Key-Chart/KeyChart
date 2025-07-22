# Script para listar e-mails e senhas de acesso dos atletas (InscricoesOnline)
# Uso: python listar_senhas_atletas.py

import os
import django
import sys

# Configurar o Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.inscricoes_online.models import InscricaoOnline

print("E-mails e senhas de acesso dos atletas cadastrados:\n")
for insc in InscricaoOnline.objects.all()[:30]:
    print(f"Email: {insc.email}\tSenha: {insc.senha_atleta}")

print("\nExibindo até 30 inscrições. Para mais, edite o script.")
