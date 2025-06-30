#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client

# Criar um cliente de teste
client = Client()

# Fazer login
print("=== TESTANDO LOGIN E PÁGINA ===")
login_data = {'username': 'Keychart', 'password': '12345'}
response = client.post('/keychart/login/', login_data)
print(f'Login response status: {response.status_code}')

# Agora acessar a página de atletas
response = client.get('/keychart/equipes_atletas/')
print(f'Página atletas status: {response.status_code}')

if response.status_code == 200:
    content_str = str(response.content)
    print(f'Conteúdo contém 999? {"999" in content_str}')
    print(f'Conteúdo contém Total de Atletas? {"Total de Atletas" in content_str}')
    
    # Procurar por parte do conteúdo para debug
    if "stat-card" in content_str:
        print("✓ Cards de estatísticas encontrados no HTML")
    else:
        print("✗ Cards de estatísticas NÃO encontrados")
        
    # Verificar se há mensagens de debug
    if "VIEW DE ATLETAS SENDO CHAMADA" in content_str:
        print("✓ Prints de debug encontrados")
    else:
        print("✗ Prints de debug NÃO encontrados")
else:
    print(f"Erro: Status {response.status_code}")
