#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append('.')
django.setup()

from app.atletas.models import Atleta

print("=== TESTE FINAL ===")
atletas = Atleta.objects.all()
print(f"Total de atletas: {atletas.count()}")

for atleta in atletas:
    print(f"- {atleta.nome_completo}: {atleta.modalidade} - {atleta.status}")

print("\n=== ESTATÍSTICAS ===")
total_atletas = Atleta.objects.count()
total_kata = Atleta.objects.filter(modalidade__in=['kata', 'ambos']).count()
total_kumite = Atleta.objects.filter(modalidade__in=['kumite', 'ambos']).count()
total_ativos = Atleta.objects.filter(status='ativo').count()

print(f"Total: {total_atletas}")
print(f"Kata: {total_kata}")
print(f"Kumite: {total_kumite}")
print(f"Ativos: {total_ativos}")
