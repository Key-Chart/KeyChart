#!/usr/bin/env python3
"""
Script para criar dados de teste para o sistema de inscrições online
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar o Django
sys.path.append('/home/rafaelti/KeyChart/BackEnd')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.competicoes.models import Competicao, Categoria, Arbitro, Academia
from app.atletas.models import Atleta

def criar_dados_teste():
    print("🚀 Criando dados de teste para inscrições online...")
    
    # Criar árbitro de teste
    arbitro, created = Arbitro.objects.get_or_create(
        email='arbitro@teste.com',
        defaults={
            'nome': 'João Silva',
            'telefone': '(11) 99999-9999'
        }
    )
    
    # Criar competições de teste com inscrições abertas
    competicoes_data = [
        {
            'nome': 'Copa Regional de Karatê 2025',
            'modalidade': 'Kata-Kumitê',
            'data_inicio': datetime.now().date() + timedelta(days=30),
            'horario': '08:00:00',
            'local': 'Ginásio Municipal - São Paulo/SP',
            'regras_especificas': 'Competição seguindo regras WKF. Obrigatório kimono branco.',
            'inscricoes_abertas': True,
            'inscricoes_status': 'abertas',
            'inscricoes_data_limite': datetime.now().date() + timedelta(days=15),
            'inscricoes_valor': Decimal('120.00'),
            'inscricoes_taxa': Decimal('5.00'),
            'inscricoes_desconto': Decimal('10.00'),
            'inscricoes_pagamento_pix': True,
            'inscricoes_pagamento_cartao': True,
            'inscricoes_pagamento_boleto': False,
            'inscricoes_mostrar_valor': True,
            'inscricoes_mostrar_vagas': True,
            'inscricoes_mensagem': 'Vagas limitadas! Garante já sua participação nesta importante competição.',
        },
        {
            'nome': 'Campeonato Estadual de Kata 2025',
            'modalidade': 'Kata',
            'data_inicio': datetime.now().date() + timedelta(days=45),
            'horario': '09:00:00',
            'local': 'Centro de Convenções - Rio de Janeiro/RJ',
            'regras_especificas': 'Apenas modalidade Kata. Atletas podem participar de múltiplas categorias.',
            'inscricoes_abertas': True,
            'inscricoes_status': 'abertas',
            'inscricoes_data_limite': datetime.now().date() + timedelta(days=20),
            'inscricoes_valor': Decimal('80.00'),
            'inscricoes_taxa': Decimal('0.00'),
            'inscricoes_desconto': Decimal('0.00'),
            'inscricoes_pagamento_pix': True,
            'inscricoes_pagamento_cartao': True,
            'inscricoes_pagamento_boleto': True,
            'inscricoes_mostrar_valor': True,
            'inscricoes_mostrar_vagas': False,
            'inscricoes_mensagem': 'Evento focado exclusivamente em Kata com premiação especial.',
        },
        {
            'nome': 'Torneio de Kumitê Juvenil 2025',
            'modalidade': 'Kumitê',
            'data_inicio': datetime.now().date() + timedelta(days=60),
            'horario': '10:00:00',
            'local': 'Complexo Esportivo - Belo Horizonte/MG',
            'regras_especificas': 'Apenas para categorias juvenis. Equipamentos de proteção obrigatórios.',
            'inscricoes_abertas': True,
            'inscricoes_status': 'abertas',
            'inscricoes_data_limite': datetime.now().date() + timedelta(days=25),
            'inscricoes_valor': Decimal('100.00'),
            'inscricoes_taxa': Decimal('8.00'),
            'inscricoes_desconto': Decimal('5.00'),
            'inscricoes_pagamento_pix': True,
            'inscricoes_pagamento_cartao': False,
            'inscricoes_pagamento_boleto': True,
            'inscricoes_mostrar_valor': True,
            'inscricoes_mostrar_vagas': True,
            'inscricoes_mensagem': 'Torneio especial para desenvolvimento dos jovens atletas.',
        }
    ]
    
    competicoes_criadas = []
    for comp_data in competicoes_data:
        competicao, created = Competicao.objects.get_or_create(
            nome=comp_data['nome'],
            defaults=comp_data
        )
        
        if created:
            print(f"✅ Competição criada: {competicao.nome}")
            # Adicionar árbitro
            competicao.arbitros.add(arbitro)
        else:
            print(f"ℹ️  Competição já existe: {competicao.nome}")
        
        competicoes_criadas.append(competicao)
    
    # Criar categorias para cada competição
    categorias_data = [
        # Categorias infantis
        {'nome': 'Infantil Masculino Kata', 'sexo': 'M', 'tipo': 'kata'},
        {'nome': 'Infantil Feminino Kata', 'sexo': 'F', 'tipo': 'kata'},
        {'nome': 'Infantil Masculino Kumitê', 'sexo': 'M', 'tipo': 'kumite'},
        {'nome': 'Infantil Feminino Kumitê', 'sexo': 'F', 'tipo': 'kumite'},
        
        # Categorias juvenis
        {'nome': 'Juvenil Masculino Kata', 'sexo': 'M', 'tipo': 'kata'},
        {'nome': 'Juvenil Feminino Kata', 'sexo': 'F', 'tipo': 'kata'},
        {'nome': 'Juvenil Masculino Kumitê -60kg', 'sexo': 'M', 'tipo': 'kumite'},
        {'nome': 'Juvenil Masculino Kumitê -70kg', 'sexo': 'M', 'tipo': 'kumite'},
        {'nome': 'Juvenil Feminino Kumitê -50kg', 'sexo': 'F', 'tipo': 'kumite'},
        {'nome': 'Juvenil Feminino Kumitê -55kg', 'sexo': 'F', 'tipo': 'kumite'},
        
        # Categorias adultas
        {'nome': 'Adulto Masculino Kata', 'sexo': 'M', 'tipo': 'kata'},
        {'nome': 'Adulto Feminino Kata', 'sexo': 'F', 'tipo': 'kata'},
        {'nome': 'Adulto Masculino Kumitê -75kg', 'sexo': 'M', 'tipo': 'kumite'},
        {'nome': 'Adulto Masculino Kumitê -85kg', 'sexo': 'M', 'tipo': 'kumite'},
        {'nome': 'Adulto Masculino Kumitê +85kg', 'sexo': 'M', 'tipo': 'kumite'},
        {'nome': 'Adulto Feminino Kumitê -60kg', 'sexo': 'F', 'tipo': 'kumite'},
        {'nome': 'Adulto Feminino Kumitê -70kg', 'sexo': 'F', 'tipo': 'kumite'},
        {'nome': 'Adulto Feminino Kumitê +70kg', 'sexo': 'F', 'tipo': 'kumite'},
    ]
    
    for competicao in competicoes_criadas:
        print(f"\n📋 Criando categorias para {competicao.nome}...")
        
        # Filtrar categorias baseado na modalidade
        if competicao.modalidade == 'Kata':
            cats_filtradas = [c for c in categorias_data if c['tipo'] == 'kata']
        elif competicao.modalidade == 'Kumitê':
            cats_filtradas = [c for c in categorias_data if c['tipo'] == 'kumite']
        else:  # Kata-Kumitê
            cats_filtradas = categorias_data
        
        for cat_data in cats_filtradas:
            categoria, created = Categoria.objects.get_or_create(
                competicao=competicao,
                nome=cat_data['nome'],
                defaults={
                    'sexo': cat_data['sexo'],
                    'tipo': cat_data['tipo']
                }
            )
            
            if created:
                print(f"  ✅ Categoria: {categoria.nome}")
    
    # Criar algumas academias de exemplo
    academias_data = [
        {'nome': 'Academia Leão Dourado', 'cidade': 'São Paulo', 'estado': 'SP'},
        {'nome': 'Dojo Samurai', 'cidade': 'Rio de Janeiro', 'estado': 'RJ'},
        {'nome': 'Centro de Karatê Tradicional', 'cidade': 'Belo Horizonte', 'estado': 'MG'},
        {'nome': 'Academia Dragão Vermelho', 'cidade': 'Porto Alegre', 'estado': 'RS'},
        {'nome': 'Dojo Águia Real', 'cidade': 'Curitiba', 'estado': 'PR'},
    ]
    
    print(f"\n🏢 Criando academias de exemplo...")
    for comp in competicoes_criadas:
        for acad_data in academias_data:
            academia, created = Academia.objects.get_or_create(
                competicao=comp,
                nome=acad_data['nome'],
                defaults={
                    'cidade': acad_data['cidade'],
                    'estado': acad_data['estado']
                }
            )
            
            if created:
                print(f"  ✅ Academia: {academia.nome} - {academia.cidade}/{academia.estado}")
    
    print(f"\n🎉 Dados de teste criados com sucesso!")
    print(f"📊 Resumo:")
    print(f"   • {len(competicoes_criadas)} competições com inscrições abertas")
    print(f"   • {Categoria.objects.count()} categorias disponíveis")
    print(f"   • {Academia.objects.count()} academias cadastradas")
    print(f"\n🌐 Acesse: http://localhost:8000/inscricoes/")

if __name__ == '__main__':
    criar_dados_teste()
