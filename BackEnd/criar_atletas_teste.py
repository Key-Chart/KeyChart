#!/usr/bin/env python
import os
import django
from datetime import date, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.atletas.models import Atleta
from app.competicoes.models import Competicao, Categoria, Academia

def criar_atletas_teste():
    # Verificar se já existem atletas
    if Atleta.objects.exists():
        print("Já existem atletas no banco. Pulando criação...")
        return
    
    # Obter ou criar competição
    competicao, created = Competicao.objects.get_or_create(
        nome='Competição Teste',
        defaults={
            'data_inicio': date.today() + timedelta(days=30),
            'data_fim': date.today() + timedelta(days=32),
            'inscricoes_abertas': True,
            'status': 'Ativa'
        }
    )
    
    # Obter ou criar categoria
    categoria, created = Categoria.objects.get_or_create(
        nome='Categoria Geral',
        defaults={
            'competicao': competicao,
            'sexo': 'X',
            'idade_min': 18,
            'idade_max': 40,
            'peso_min': 50,
            'peso_max': 100,
            'tipo': 'kumite'
        }
    )
    
    # Obter ou criar academia
    academia, created = Academia.objects.get_or_create(
        nome='Academia Teste',
        defaults={
            'cidade': 'São Paulo',
            'estado': 'SP',
            'telefone': '(11) 99999-9999',
            'email': 'teste@academia.com'
        }
    )
    
    # Dados de atletas de teste
    atletas_dados = [
        {
            'nome_completo': 'João Silva Santos',
            'data_nascimento': date(1995, 3, 15),
            'sexo': 'M',
            'modalidade': 'kumite',
            'status': 'ativo',
            'faixa': 'preta',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'email': 'joao.silva@email.com',
            'telefone': '(11) 98765-4321'
        },
        {
            'nome_completo': 'Maria Oliveira Costa',
            'data_nascimento': date(1992, 7, 22),
            'sexo': 'F',
            'modalidade': 'kata',
            'status': 'ativo',
            'faixa': 'marrom',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'email': 'maria.oliveira@email.com',
            'telefone': '(21) 97654-3210'
        },
        {
            'nome_completo': 'Pedro Ferreira Lima',
            'data_nascimento': date(1998, 12, 8),
            'sexo': 'M',
            'modalidade': 'ambos',
            'status': 'ativo',
            'faixa': 'azul',
            'cidade': 'Belo Horizonte',
            'estado': 'MG',
            'email': 'pedro.ferreira@email.com',
            'telefone': '(31) 96543-2109'
        },
        {
            'nome_completo': 'Ana Paula Rodrigues',
            'data_nascimento': date(1990, 5, 30),
            'sexo': 'F',
            'modalidade': 'kata',
            'status': 'inativo',
            'faixa': 'preta',
            'cidade': 'Salvador',
            'estado': 'BA',
            'email': 'ana.paula@email.com',
            'telefone': '(71) 95432-1098'
        },
        {
            'nome_completo': 'Carlos Eduardo Souza',
            'data_nascimento': date(1985, 11, 18),
            'sexo': 'M',
            'modalidade': 'kumite',
            'status': 'ativo',
            'faixa': 'preta',
            'cidade': 'Porto Alegre',
            'estado': 'RS',
            'email': 'carlos.souza@email.com',
            'telefone': '(51) 94321-0987'
        },
        {
            'nome_completo': 'Larissa Martins Silva',
            'data_nascimento': date(2000, 2, 14),
            'sexo': 'F',
            'modalidade': 'ambos',
            'status': 'ativo',
            'faixa': 'verde',
            'cidade': 'Curitiba',
            'estado': 'PR',
            'email': 'larissa.martins@email.com',
            'telefone': '(41) 93210-9876'
        },
        {
            'nome_completo': 'Rafael Almeida Nunes',
            'data_nascimento': date(1993, 9, 25),
            'sexo': 'M',
            'modalidade': 'kata',
            'status': 'inativo',
            'faixa': 'roxa',
            'cidade': 'Recife',
            'estado': 'PE',
            'email': 'rafael.almeida@email.com',
            'telefone': '(81) 92109-8765'
        },
        {
            'nome_completo': 'Juliana Santos Pereira',
            'data_nascimento': date(1996, 4, 12),
            'sexo': 'F',
            'modalidade': 'kumite',
            'status': 'ativo',
            'faixa': 'marrom',
            'cidade': 'Fortaleza',
            'estado': 'CE',
            'email': 'juliana.santos@email.com',
            'telefone': '(85) 91098-7654'
        }
    ]
    
    # Criar atletas
    for dados in atletas_dados:
        atleta = Atleta.objects.create(
            competicao=competicao,
            categoria=categoria,
            academia=academia,
            peso=random.randint(55, 85),
            altura=random.randint(160, 185),
            **dados
        )
        print(f"Atleta criado: {atleta.nome_completo}")
    
    print(f"\nTotal de atletas criados: {len(atletas_dados)}")
    print(f"Atletas ativos: {Atleta.objects.filter(status='ativo').count()}")
    print(f"Atletas inativos: {Atleta.objects.filter(status='inativo').count()}")
    print(f"Modalidade Kata: {Atleta.objects.filter(modalidade='kata').count()}")
    print(f"Modalidade Kumite: {Atleta.objects.filter(modalidade='kumite').count()}")
    print(f"Modalidade Ambos: {Atleta.objects.filter(modalidade='ambos').count()}")

if __name__ == '__main__':
    criar_atletas_teste()
