#!/usr/bin/env python
"""
Script para testar o sistema completo de inscrições online
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.competicoes.models import Competicao, Academia
from app.inscricoes_online.models import InscricaoOnline
from app.atletas.models import Atleta
from datetime import datetime, timedelta
import uuid

def testar_sistema():
    print("=== TESTE DO SISTEMA DE INSCRIÇÕES ONLINE ===\n")
    
    # 1. Verificar competições disponíveis
    print("1. Verificando competições disponíveis:")
    competicoes = Competicao.objects.filter(
        data_inicio__gte=datetime.now(),
        status='Ativa'
    )
    print(f"   - Competições futuras ativas: {competicoes.count()}")
    
    if competicoes.exists():
        comp_teste = competicoes.first()
        print(f"   - Competição para teste: {comp_teste.nome}")
        print(f"   - Data: {comp_teste.data_inicio}")
        print(f"   - Local: {comp_teste.local}")
        
        # 2. Testar criação de inscrição
        print("\n2. Testando criação de inscrição:")
        
        # Verificar se já existe uma academia de teste
        academia_teste = Academia.objects.filter(
            competicao=comp_teste,
            nome="Academia Teste Inscrições"
        ).first()
        if not academia_teste:
            academia_teste = Academia.objects.create(
                competicao=comp_teste,
                nome="Academia Teste Inscrições",
                endereco="Rua Teste, 123",
                cidade="São Paulo",
                estado="SP"
            )
            print(f"   - Academia de teste criada: {academia_teste.nome}")
        else:
            print(f"   - Usando academia existente: {academia_teste.nome}")
        
        # Verificar se existe categoria para a competição
        categoria_teste = comp_teste.categorias.first()
        if not categoria_teste:
            print("   - AVISO: Competição não possui categorias cadastradas!")
            return
        
        # Criar dados de teste para inscrição
        dados_teste = {
            'competicao': comp_teste,
            'categoria': categoria_teste,
            'nome_completo': 'João da Silva Teste',
            'cpf': '123.456.789-00',
            'data_nascimento': '2000-01-15',
            'sexo': 'M',
            'email': 'joao.teste@email.com',
            'telefone': '(11) 99999-9999',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'faixa': 'marrom',
            'peso': 75.5,
            'altura': 175,
            'academia_nome': academia_teste.nome,
            'academia_cidade': academia_teste.cidade,
            'academia_estado': academia_teste.estado,
            'academia': academia_teste,
            'forma_pagamento': 'pix',
            'valor_inscricao': 50.00,
        }
        
        # Verificar se já existe inscrição para este email
        inscricao_existente = InscricaoOnline.objects.filter(
            competicao=comp_teste,
            email=dados_teste['email']
        ).first()
        
        if inscricao_existente:
            print(f"   - Inscrição já existe: {inscricao_existente.id}")
            print(f"   - Status: {inscricao_existente.status}")
            inscricao_teste = inscricao_existente
        else:
            # Criar nova inscrição
            try:
                inscricao_teste = InscricaoOnline.objects.create(**dados_teste)
                print(f"   - Inscrição criada com sucesso: {inscricao_teste.id}")
                print(f"   - Status: {inscricao_teste.status}")
                print(f"   - Senha do atleta: {inscricao_teste.senha_atleta}")
            except Exception as e:
                print(f"   - ERRO ao criar inscrição: {e}")
                return
        
        # 3. Verificar URLs funcionando
        print("\n3. URLs disponíveis para teste:")
        print(f"   - Lista de competições: http://localhost:8000/inscricoes/")
        print(f"   - Inscrição na competição: http://localhost:8000/inscricoes/competicao/{comp_teste.id}/")
        print(f"   - Status da inscrição: http://localhost:8000/inscricoes/status/{inscricao_teste.id}/")
        
        # 4. Verificar integração com atletas
        print("\n4. Verificando integração com sistema de atletas:")
        atleta_integrado = Atleta.objects.filter(email=dados_teste['email']).first()
        if atleta_integrado:
            print(f"   - Atleta encontrado no sistema: {atleta_integrado.nome}")
            print(f"   - ID do atleta: {atleta_integrado.id}")
        else:
            print("   - Atleta ainda não integrado (será criado no processamento)")
        
        # 5. Estatísticas gerais
        print("\n5. Estatísticas do sistema:")
        total_inscricoes = InscricaoOnline.objects.count()
        inscricoes_pendentes = InscricaoOnline.objects.filter(status='pendente').count()
        inscricoes_aprovadas = InscricaoOnline.objects.filter(status='aprovada').count()
        
        print(f"   - Total de inscrições: {total_inscricoes}")
        print(f"   - Inscrições pendentes: {inscricoes_pendentes}")
        print(f"   - Inscrições aprovadas: {inscricoes_aprovadas}")
        
    else:
        print("   - AVISO: Nenhuma competição futura encontrada!")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == '__main__':
    testar_sistema()
