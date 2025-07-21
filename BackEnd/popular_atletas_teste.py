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

def popular_atletas_teste():
    print("Populando banco com atletas de teste...")
    
    # Obter ou criar competição
    competicao, created = Competicao.objects.get_or_create(
        nome='Competição Teste',
        defaults={
            'modalidade': 'Karatê',
            'data_inicio': date.today() + timedelta(days=30),
            'horario': '08:00',
            'local': 'Ginásio Municipal',
            'inscricoes_abertas': True,
            'status': 'Ativa'
        }
    )
    
    # Criar categorias
    categoria_kata, created = Categoria.objects.get_or_create(
        nome='Kata Geral',
        defaults={
            'competicao': competicao,
            'sexo': 'MX',
            'tipo': 'GI'
        }
    )
    
    categoria_kumite, created = Categoria.objects.get_or_create(
        nome='Kumite Geral',
        defaults={
            'competicao': competicao,
            'sexo': 'MX',
            'tipo': 'GI'
        }
    )
    
    # Criar academias
    academia1, created = Academia.objects.get_or_create(
        nome='Academia Central',
        defaults={
            'competicao': competicao,
            'cidade': 'São Paulo',
            'estado': 'SP',
            'endereco': 'Rua da Academia, 123'
        }
    )
    
    academia2, created = Academia.objects.get_or_create(
        nome='Clube de Karatê',
        defaults={
            'competicao': competicao,
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'endereco': 'Av. do Karatê, 456'
        }
    )
    
    # Dados de atletas de teste
    atletas_dados = [
        {
            'nome_completo': 'João Silva Santos',
            'data_nascimento': date(1995, 3, 15),
            'sexo': 'M',
            'idade': 28,
            'faixa': 'preta',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'email': 'joao.silva@email.com',
            'telefone': '(11) 98765-4321',
            'categoria': categoria_kumite,
            'academia': academia1,
            'ativo': True
        },
        {
            'nome_completo': 'Maria Oliveira Costa',
            'data_nascimento': date(1992, 7, 22),
            'sexo': 'F',
            'idade': 31,
            'faixa': 'marrom',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'email': 'maria.oliveira@email.com',
            'telefone': '(21) 97654-3210',
            'categoria': categoria_kata,
            'academia': academia2,
            'ativo': True
        },
        {
            'nome_completo': 'Pedro Ferreira Lima',
            'data_nascimento': date(1998, 12, 8),
            'sexo': 'M',
            'idade': 25,
            'faixa': 'azul',
            'cidade': 'Belo Horizonte',
            'estado': 'MG',
            'email': 'pedro.ferreira@email.com',
            'telefone': '(31) 96543-2109',
            'categoria': categoria_kumite,
            'academia': academia1,
            'ativo': True
        },
        {
            'nome_completo': 'Ana Paula Rodrigues',
            'data_nascimento': date(1990, 5, 30),
            'sexo': 'F',
            'idade': 33,
            'faixa': 'preta',
            'cidade': 'Salvador',
            'estado': 'BA',
            'email': 'ana.paula@email.com',
            'telefone': '(71) 95432-1098',
            'categoria': categoria_kata,
            'academia': academia2,
            'ativo': False,  # Atleta inativo
            'motivo_inativacao': 'Lesão temporária'
        },
        {
            'nome_completo': 'Carlos Eduardo Souza',
            'data_nascimento': date(1985, 11, 18),
            'sexo': 'M',
            'idade': 38,
            'faixa': 'preta',
            'cidade': 'Porto Alegre',
            'estado': 'RS',
            'email': 'carlos.souza@email.com',
            'telefone': '(51) 94321-0987',
            'categoria': categoria_kumite,
            'academia': academia1,
            'ativo': True
        },
        {
            'nome_completo': 'Larissa Martins Silva',
            'data_nascimento': date(1996, 9, 14),
            'sexo': 'F',
            'idade': 27,
            'faixa': 'roxa',
            'cidade': 'Brasília',
            'estado': 'DF',
            'email': 'larissa.martins@email.com',
            'telefone': '(61) 93210-9876',
            'categoria': categoria_kata,
            'academia': academia2,
            'ativo': False,  # Atleta inativo
            'motivo_inativacao': 'Mudança de cidade'
        },
        {
            'nome_completo': 'Roberto Santos Lima',
            'data_nascimento': date(1993, 1, 25),
            'sexo': 'M',
            'idade': 30,
            'faixa': 'marrom',
            'cidade': 'Recife',
            'estado': 'PE',
            'email': 'roberto.santos@email.com',
            'telefone': '(81) 92109-8765',
            'categoria': categoria_kumite,
            'academia': academia1,
            'ativo': True
        },
        {
            'nome_completo': 'Juliana Santos Pereira',
            'data_nascimento': date(1996, 4, 12),
            'sexo': 'F',
            'idade': 27,
            'faixa': 'marrom',
            'cidade': 'Fortaleza',
            'estado': 'CE',
            'email': 'juliana.santos@email.com',
            'telefone': '(85) 91098-7654',
            'categoria': categoria_kata,
            'academia': academia2,
            'ativo': True
        }
    ]
    
    # Criar atletas se não existirem
    for dados in atletas_dados:
        atleta, created = Atleta.objects.get_or_create(
            nome_completo=dados['nome_completo'],
            defaults={
                'competicao': competicao,
                'categoria': dados['categoria'],
                'academia': dados['academia'],
                'data_nascimento': dados['data_nascimento'],
                'sexo': dados['sexo'],
                'idade': dados['idade'],
                'peso': random.randint(55, 85),
                'altura': random.randint(160, 185),
                'email': dados['email'],
                'telefone': dados['telefone'],
                'faixa': dados['faixa'],
                'cidade': dados['cidade'],
                'estado': dados['estado'],
                'ativo': dados['ativo'],
                'motivo_inativacao': dados.get('motivo_inativacao', '')
            }
        )
        
        if created:
            print(f"Atleta criado: {atleta.nome_completo} ({'Ativo' if atleta.ativo else 'Inativo'})")
        else:
            print(f"Atleta já existe: {atleta.nome_completo}")
    
    print(f"\nResumo:")
    print(f"Total de atletas: {Atleta.objects.count()}")
    print(f"Atletas ativos: {Atleta.objects.filter(ativo=True).count()}")
    print(f"Atletas inativos: {Atleta.objects.filter(ativo=False).count()}")
    print(f"Categoria Kata: {Atleta.objects.filter(categoria__nome__icontains='Kata').count()}")
    print(f"Categoria Kumite: {Atleta.objects.filter(categoria__nome__icontains='Kumite').count()}")

if __name__ == '__main__':
    popular_atletas_teste()
