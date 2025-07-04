#!/usr/bin/env python
"""
Script para criar dados de teste para o sistema de partidas
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
sys.path.append('/home/rafaelti/Documentos/Keychart/KeyChart/BackEnd')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.competicoes.models import Competicao, Categoria, PartidaKumite
from app.atletas.models import Atleta, Academia

def criar_dados_teste():
    print("Criando dados de teste...")
    
    # Verificar se já existem dados
    if PartidaKumite.objects.count() > 0:
        print(f"Já existem {PartidaKumite.objects.count()} partidas no banco.")
        return
    
    try:
        # Criar competição se não existir
        competicao, created = Competicao.objects.get_or_create(
            nome="Copa Regional 2025",
            defaults={
                'modalidade': 'Karatê',
                'data_inicio': datetime.now().date(),
                'horario': datetime.now().time(),
                'local': 'Centro de Convenções',
                'status': 'Ativa'
            }
        )
        
        if created:
            print(f"Competição criada: {competicao.nome}")
        
        # Criar categoria se não existir
        categoria, created = Categoria.objects.get_or_create(
            competicao=competicao,
            nome="Kata Individual - Faixa Preta",
            defaults={
                'sexo': 'M',
                'tipo': 'GI'
            }
        )
        
        if created:
            print(f"Categoria criada: {categoria.nome}")
        
        # Criar academia se não existir
        academia, created = Academia.objects.get_or_create(
            competicao=competicao,
            nome="Academia Teste",
            defaults={
                'cidade': 'São Paulo',
                'estado': 'SP'
            }
        )
        
        if created:
            print(f"Academia criada: {academia.nome}")
        
        # Criar atletas se não existirem
        atleta1, created = Atleta.objects.get_or_create(
            nome_completo="João Silva",
            defaults={
                'academia': academia,
                'cpf': '12345678901',
                'data_nascimento': datetime.now().date() - timedelta(days=365*25),
                'telefone': '11999999999',
                'email': 'joao@teste.com'
            }
        )
        
        if created:
            print(f"Atleta criado: {atleta1.nome_completo}")
        
        atleta2, created = Atleta.objects.get_or_create(
            nome_completo="Maria Santos",
            defaults={
                'academia': academia,
                'cpf': '12345678902',
                'data_nascimento': datetime.now().date() - timedelta(days=365*23),
                'telefone': '11888888888',
                'email': 'maria@teste.com'
            }
        )
        
        if created:
            print(f"Atleta criado: {atleta2.nome_completo}")
        
        # Criar partida de teste
        partida = PartidaKumite.objects.create(
            categoria=categoria,
            competicao=competicao,
            fase="Final",
            round_numero=1,
            atleta1=atleta1,
            atleta2=atleta2,
            status='em_andamento',
            pontos_atleta1=5,
            pontos_atleta2=3,
            data_inicio=datetime.now()
        )
        
        print(f"Partida criada: ID {partida.id} - {atleta1.nome_completo} vs {atleta2.nome_completo}")
        print(f"Status: {partida.status}")
        print(f"Placar: {partida.pontos_atleta1} x {partida.pontos_atleta2}")
        
    except Exception as e:
        print(f"Erro ao criar dados de teste: {e}")

if __name__ == "__main__":
    criar_dados_teste()
