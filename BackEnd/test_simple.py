#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append('.')
django.setup()

from app.atletas.models import Atleta

print("=== TESTE SIMPLES ===")
total_atletas = Atleta.objects.count()
total_kata = Atleta.objects.filter(modalidade__in=['kata', 'ambos']).count()
total_kumite = Atleta.objects.filter(modalidade__in=['kumite', 'ambos']).count()
total_ativos = Atleta.objects.filter(status='ativo').count()

print(f"Total de atletas: {total_atletas}")
print(f"Total kata: {total_kata}")
print(f"Total kumite: {total_kumite}")
print(f"Total ativos: {total_ativos}")

# Listar alguns atletas para verificar
print("\n=== ATLETAS ===")
for atleta in Atleta.objects.all()[:5]:
    print(f"{atleta.nome_completo} - {atleta.modalidade} - {atleta.status}")
