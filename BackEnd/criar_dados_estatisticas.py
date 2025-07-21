#!/usr/bin/env python
"""
Script para criar dados de teste para o sistema de estatísticas
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append('/home/rafaelti/KeyChart/BackEnd')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.competicoes.models import Competicao, Categoria, Academia, Arbitro
from app.atletas.models import Atleta
from django.utils import timezone

def criar_dados_teste():
    """Criar dados de teste para o sistema de estatísticas"""
    print("🔄 Criando dados de teste para estatísticas...")
    
    # Criar árbitros
    arbitros = []
    nomes_arbitros = ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa']
    for nome in nomes_arbitros:
        arbitro, created = Arbitro.objects.get_or_create(
            nome=nome,
            defaults={
                'email': f'{nome.lower().replace(" ", ".")}@email.com',
                'telefone': f'11999{random.randint(100000, 999999)}'
            }
        )
        arbitros.append(arbitro)
        if created:
            print(f"  ✅ Árbitro criado: {nome}")
    
    # Criar competições
    competicoes_dados = [
        {
            'nome': 'Campeonato Estadual de Karatê 2025',
            'modalidade': 'Karatê',
            'data_inicio': timezone.now().date() - timedelta(days=30),
            'local': 'São Paulo - SP'
        },
        {
            'nome': 'Copa Brasileira de Karatê',
            'modalidade': 'Karatê',
            'data_inicio': timezone.now().date() - timedelta(days=15),
            'local': 'Rio de Janeiro - RJ'
        },
        {
            'nome': 'Torneio Regional Nordeste',
            'modalidade': 'Karatê',
            'data_inicio': timezone.now().date() + timedelta(days=10),
            'local': 'Salvador - BA'
        },
        {
            'nome': 'Championship Sul-Americano',
            'modalidade': 'Karatê',
            'data_inicio': timezone.now().date() + timedelta(days=45),
            'local': 'Curitiba - PR'
        }
    ]
    
    competicoes = []
    for dados in competicoes_dados:
        competicao, created = Competicao.objects.get_or_create(
            nome=dados['nome'],
            defaults={
                'modalidade': dados['modalidade'],
                'data_inicio': dados['data_inicio'],
                'horario': '09:00',
                'local': dados['local'],
                'status': 'Ativa' if dados['data_inicio'] >= timezone.now().date() else 'Finalizada',
                'inscricoes_abertas': dados['data_inicio'] >= timezone.now().date(),
                'inscricoes_valor': 120.00
            }
        )
        competicao.arbitros.set(random.sample(arbitros, k=random.randint(1, 3)))
        competicoes.append(competicao)
        if created:
            print(f"  ✅ Competição criada: {dados['nome']}")
    
    # Criar categorias para cada competição
    categorias_base = [
        {'nome': 'Infantil Masculino', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Infantil Feminino', 'sexo': 'F', 'tipo': 'GI'},
        {'nome': 'Juvenil Masculino', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Juvenil Feminino', 'sexo': 'F', 'tipo': 'GI'},
        {'nome': 'Adulto Masculino', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Adulto Feminino', 'sexo': 'F', 'tipo': 'GI'},
        {'nome': 'Master Masculino', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Master Feminino', 'sexo': 'F', 'tipo': 'GI'},
    ]
    
    categorias = []
    for competicao in competicoes:
        for cat_dados in categorias_base:
            categoria, created = Categoria.objects.get_or_create(
                competicao=competicao,
                nome=cat_dados['nome'],
                defaults={
                    'sexo': cat_dados['sexo'],
                    'tipo': cat_dados['tipo']
                }
            )
            categorias.append(categoria)
            if created:
                print(f"    ✅ Categoria criada: {cat_dados['nome']} - {competicao.nome}")
    
    # Criar academias
    academias_dados = [
        {'nome': 'Academia Dragão Dourado', 'cidade': 'São Paulo', 'estado': 'SP'},
        {'nome': 'Centro de Karatê Ippon', 'cidade': 'Rio de Janeiro', 'estado': 'RJ'},
        {'nome': 'Dojo Tradicional Kyokushin', 'cidade': 'Belo Horizonte', 'estado': 'MG'},
        {'nome': 'Academia Samurai', 'cidade': 'Salvador', 'estado': 'BA'},
        {'nome': 'Karatê-Do Shotokan', 'cidade': 'Curitiba', 'estado': 'PR'},
        {'nome': 'Dojo Bushido', 'cidade': 'Porto Alegre', 'estado': 'RS'},
        {'nome': 'Academia Phoenix', 'cidade': 'Recife', 'estado': 'PE'},
        {'nome': 'Centro Marcial Tigre', 'cidade': 'Fortaleza', 'estado': 'CE'},
    ]
    
    academias = []
    for competicao in competicoes:
        for acad_dados in academias_dados:
            academia, created = Academia.objects.get_or_create(
                competicao=competicao,
                nome=acad_dados['nome'],
                defaults={
                    'cidade': acad_dados['cidade'],
                    'estado': acad_dados['estado'],
                    'endereco': f"Rua das Artes Marciais, {random.randint(100, 999)}"
                }
            )
            academias.append(academia)
            if created:
                print(f"    ✅ Academia criada: {acad_dados['nome']} - {competicao.nome}")
    
    # Criar atletas
    nomes_masculinos = [
        'João Silva', 'Pedro Santos', 'Carlos Oliveira', 'Roberto Costa', 'Eduardo Lima',
        'Fernando Souza', 'Marcos Pereira', 'Luiz Almeida', 'Rafael Ribeiro', 'Thiago Martins',
        'Gustavo Ferreira', 'Bruno Rodrigues', 'Leonardo Dias', 'Henrique Barbosa', 'Victor Hugo',
        'Gabriel Nascimento', 'Diego Cardoso', 'Mateus Gomes', 'Lucas Monteiro', 'André Felipe'
    ]
    
    nomes_femininos = [
        'Maria Silva', 'Ana Santos', 'Carla Oliveira', 'Roberta Costa', 'Eduarda Lima',
        'Fernanda Souza', 'Marcela Pereira', 'Luiza Almeida', 'Rafaela Ribeiro', 'Thais Martins',
        'Gustava Ferreira', 'Bruna Rodrigues', 'Leticia Dias', 'Henrica Barbosa', 'Vitoria Hugo',
        'Gabriela Nascimento', 'Diana Cardoso', 'Mariana Gomes', 'Larissa Monteiro', 'Andreia Felipe'
    ]
    
    faixas = ['BRANCA', 'AZUL', 'ROXA', 'MARROM', 'PRETA']
    estados = ['SP', 'RJ', 'MG', 'BA', 'PR', 'RS', 'PE', 'CE', 'GO', 'SC']
    
    total_atletas = 0
    for competicao in competicoes:
        comp_categorias = categorias.filter(competicao=competicao)
        comp_academias = academias.filter(competicao=competicao)
        
        for categoria in comp_categorias:
            # Número aleatório de atletas por categoria (5-15)
            num_atletas = random.randint(5, 15)
            
            for i in range(num_atletas):
                # Escolher nome baseado no sexo da categoria
                if categoria.sexo == 'M':
                    nome = random.choice(nomes_masculinos)
                    sexo = 'M'
                else:
                    nome = random.choice(nomes_femininos)
                    sexo = 'F'
                
                # Gerar dados aleatórios
                idade = random.randint(18, 45)
                data_nascimento = timezone.now().date() - timedelta(days=365*idade + random.randint(0, 365))
                peso = round(random.uniform(55.0, 95.0), 2)
                altura = random.randint(160, 190)
                faixa = random.choice(faixas)
                estado = random.choice(estados)
                academia = random.choice(comp_academias)
                
                # Data de inscrição variada (últimos 3 meses)
                data_inscricao = timezone.now() - timedelta(days=random.randint(1, 90))
                
                atleta, created = Atleta.objects.get_or_create(
                    competicao=competicao,
                    categoria=categoria,
                    nome_completo=f"{nome} {random.randint(1, 999):03d}",
                    defaults={
                        'data_nascimento': data_nascimento,
                        'sexo': sexo,
                        'idade': idade,
                        'peso': peso,
                        'altura': altura,
                        'email': f"{nome.lower().replace(' ', '.')}{random.randint(1, 999)}@email.com",
                        'telefone': f"11999{random.randint(100000, 999999)}",
                        'faixa': faixa,
                        'cidade': academia.cidade,
                        'estado': estado,
                        'academia': academia,
                        'ativo': random.choice([True, True, True, False]),  # 75% ativos
                        'data_inscricao': data_inscricao
                    }
                )
                
                if created:
                    total_atletas += 1
    
    print(f"\n📊 Dados de teste criados com sucesso!")
    print(f"   • Árbitros: {len(arbitros)}")
    print(f"   • Competições: {len(competicoes)}")
    print(f"   • Categorias: {Categoria.objects.count()}")
    print(f"   • Academias: {Academia.objects.count()}")
    print(f"   • Atletas: {total_atletas}")
    print(f"\n🎯 Sistema pronto para demonstração de estatísticas!")

if __name__ == '__main__':
    criar_dados_teste()
