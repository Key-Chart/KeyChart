#!/usr/bin/env python
"""
Script atualizado para testar o Portal do Atleta completo
Cria dados de teste e demonstra todas as funcionalidades implementadas
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configuração do Django
sys.path.append('/home/rafaelti/KeyChart/BackEnd')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from app.portal_atleta.models import AtletaUser, NotificacaoAtleta, PreferenciaAtleta
from app.inscricoes_online.models import InscricaoOnline, Competicao, Categoria

def criar_dados_completos():
    """Cria um conjunto completo de dados de teste"""
    print("🚀 Criando dados completos para o Portal do Atleta...")
    
    # 1. Criar competições variadas
    competicoes_data = [
        {
            'nome': 'Campeonato Paulista de Karatê 2025',
            'descricao': 'Campeonato estadual de karatê com modalidades kata e kumite',
            'local': 'Centro de Convenções Ibirapuera - São Paulo, SP',
            'valor_inscricao': 150.00,
            'dias_limite': 15,
            'dias_evento': 30,
            'status': 'ativa'
        },
        {
            'nome': 'Copa Brasil de Karatê Tradicional',
            'descricao': 'Competição nacional focada no karatê tradicional',
            'local': 'Ginásio do Ibirapuera - São Paulo, SP',
            'valor_inscricao': 200.00,
            'dias_limite': 20,
            'dias_evento': 45,
            'status': 'ativa'
        },
        {
            'nome': 'Torneio Regional Sul-Sudeste',
            'descricao': 'Torneio regional com atletas do Sul e Sudeste',
            'local': 'Complexo Esportivo - Curitiba, PR',
            'valor_inscricao': 120.00,
            'dias_limite': 10,
            'dias_evento': 60,
            'status': 'ativa'
        },
        {
            'nome': 'Open de Karatê Rio 2024',
            'descricao': 'Competição já realizada no Rio de Janeiro',
            'local': 'Maracanãzinho - Rio de Janeiro, RJ',
            'valor_inscricao': 180.00,
            'dias_limite': -30,
            'dias_evento': -15,
            'status': 'encerrada'
        }
    ]
    
    competicoes_criadas = []
    for comp_data in competicoes_data:
        competicao, created = Competicao.objects.get_or_create(
            nome=comp_data['nome'],
            defaults={
                'modalidade': 'Karatê',
                'data_inicio': timezone.now().date() + timedelta(days=comp_data['dias_evento']),
                'horario': timezone.now().time().replace(hour=8, minute=0),
                'local': comp_data['local'],
                'inscricoes_valor': comp_data['valor_inscricao'],
                'inscricoes_data_limite': timezone.now().date() + timedelta(days=comp_data['dias_limite']),
                'status': 'Ativa' if comp_data['status'] == 'ativa' else 'Finalizada',
                'regras_especificas': f'Regulamento da competição {comp_data["nome"]}. Todas as categorias seguem as regras oficiais da WKF.',
                'inscricoes_abertas': comp_data['status'] == 'ativa',
                'inscricoes_status': 'abertas' if comp_data['status'] == 'ativa' else 'fechadas'
            }
        )
        competicoes_criadas.append(competicao)
        if created:
            print(f"✅ Competição criada: {competicao.nome}")
    
    # 2. Criar categorias para cada competição
    categorias_templates = [
        {'nome': 'Kata Individual Masculino Adulto', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Kata Individual Feminino Adulto', 'sexo': 'F', 'tipo': 'GI'},
        {'nome': 'Kumite Masculino -75kg', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Kumite Feminino -61kg', 'sexo': 'F', 'tipo': 'GI'},
        {'nome': 'Kata Juvenil Masculino', 'sexo': 'M', 'tipo': 'GI'},
        {'nome': 'Kata Juvenil Feminino', 'sexo': 'F', 'tipo': 'GI'},
    ]
    
    for competicao in competicoes_criadas:
        for cat_data in categorias_templates:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                competicao=competicao,
                defaults={
                    'sexo': cat_data['sexo'],
                    'tipo': cat_data['tipo'],
                }
            )
            if created:
                print(f"  ➡️ Categoria criada: {categoria.nome}")
    
    # 3. Criar atletas de teste
    atletas_data = [
        {
            'nome': 'Rafael Santos Silva',
            'email': 'rafael.santos@email.com',
            'telefone': '(11) 99999-1111',
            'senha': 'senha123'
        },
        {
            'nome': 'Ana Carolina Oliveira',
            'email': 'ana.oliveira@email.com',
            'telefone': '(11) 99999-2222',
            'senha': 'senha456'
        },
        {
            'nome': 'Carlos Eduardo Lima',
            'email': 'carlos.lima@email.com',
            'telefone': '(11) 99999-3333',
            'senha': 'senha789'
        }
    ]
    
    atletas_criados = []
    for atleta_data in atletas_data:
        # Criar inscrições primeiro
        for i, competicao in enumerate(competicoes_criadas[:3]):  # 3 competições por atleta
            categoria = competicao.categorias.first()
            if categoria:
                inscricao, created = InscricaoOnline.objects.get_or_create(
                    email=atleta_data['email'],
                    competicao=competicao,
                    defaults={
                        'nome_completo': atleta_data['nome'],
                        'data_nascimento': timezone.now().date() - timedelta(days=25*365),  # 25 anos
                        'sexo': 'M' if 'Carlos' in atleta_data['nome'] or 'Rafael' in atleta_data['nome'] else 'F',
                        'telefone': atleta_data['telefone'],
                        'categoria': categoria,
                        'faixa': 'preta',
                        'peso': 70.5,
                        'altura': 175,
                        'cidade': 'São Paulo',
                        'estado': 'SP',
                        'academia_nome': 'Academia Teste',
                        'academia_cidade': 'São Paulo',
                        'academia_estado': 'SP',
                        'senha_atleta': atleta_data['senha'],
                        'valor_inscricao': competicao.inscricoes_valor,
                        'status': ['pendente', 'pago', 'confirmado'][i % 3],  # Variar status
                        'data_inscricao': timezone.now() - timedelta(days=i*10),
                    }
                )
                if created:
                    print(f"  📝 Inscrição criada: {atleta_data['nome']} -> {competicao.nome}")
        
        # Criar usuário atleta
        first_inscricao = InscricaoOnline.objects.filter(email=atleta_data['email']).first()
        if first_inscricao:
            atleta_user, created = AtletaUser.objects.get_or_create(
                email=atleta_data['email'],
                defaults={
                    'nome_completo': atleta_data['nome'],
                    'telefone': atleta_data['telefone'],
                    'inscricao_origem': first_inscricao,
                }
            )
        
        if created:
            print(f"👤 Atleta criado: {atleta_user.nome_completo}")
            
            # Criar preferências
            PreferenciaAtleta.objects.get_or_create(
                atleta=atleta_user,
                defaults={
                    'receber_email_inscricao': True,
                    'receber_email_pagamento': True,
                    'receber_email_competicao': True,
                    'receber_email_resultado': True,
                    'tema_escuro': False,
                    'idioma': 'pt-br'
                }
            )
            
            # Criar notificações de exemplo
            notificacoes_exemplo = [
                {
                    'tipo': 'sistema',
                    'titulo': 'Bem-vindo ao Portal!',
                    'mensagem': f'Olá {atleta_user.nome_completo}! Seja bem-vindo ao seu portal personalizado.',
                    'prioridade': 'alta'
                },
                {
                    'tipo': 'competicao',
                    'titulo': 'Nova competição disponível',
                    'mensagem': 'Inscrições abertas para o Campeonato Estadual de Karatê 2025.',
                    'prioridade': 'media'
                },
                {
                    'tipo': 'inscricao',
                    'titulo': 'Pagamento confirmado',
                    'mensagem': 'Seu pagamento foi processado com sucesso!',
                    'prioridade': 'alta'
                },
                {
                    'tipo': 'lembrete',
                    'titulo': 'Competição se aproxima',
                    'mensagem': 'Sua próxima competição acontece em 15 dias.',
                    'prioridade': 'media'
                }
            ]
            
            for i, notif_data in enumerate(notificacoes_exemplo):
                NotificacaoAtleta.objects.create(
                    atleta=atleta_user,
                    tipo=notif_data['tipo'],
                    titulo=notif_data['titulo'],
                    mensagem=notif_data['mensagem'],
                    prioridade=notif_data['prioridade'],
                    lida=i > 1,  # Primeiras 2 não lidas
                    data_criacao=timezone.now() - timedelta(hours=i*2)
                )
        
        atletas_criados.append(atleta_user)
    
    print(f"\n✅ Dados de teste criados com sucesso!")
    print(f"📊 Resumo:")
    print(f"   - {len(competicoes_criadas)} competições")
    print(f"   - {Categoria.objects.count()} categorias")
    print(f"   - {len(atletas_criados)} atletas")
    print(f"   - {InscricaoOnline.objects.count()} inscrições")
    print(f"   - {NotificacaoAtleta.objects.count()} notificações")
    
    return atletas_criados

def testar_funcionalidades():
    """Testa as principais funcionalidades do portal"""
    print("\n🧪 Testando funcionalidades do Portal do Atleta...")
    
    atletas = AtletaUser.objects.all()
    if not atletas:
        print("❌ Nenhum atleta encontrado. Execute criar_dados_completos() primeiro.")
        return
    
    atleta = atletas.first()
    print(f"🔍 Testando com atleta: {atleta.nome_completo}")
    
    # Testar estatísticas
    inscricoes = atleta.get_inscricoes()
    print(f"   - Total de inscrições: {inscricoes.count()}")
    print(f"   - Inscrições pagas: {inscricoes.filter(status='pago').count()}")
    print(f"   - Notificações não lidas: {atleta.notificacoes.filter(lida=False).count()}")
    
    # Testar competições
    competicoes_disponiveis = Competicao.objects.filter(status='ativa').count()
    print(f"   - Competições disponíveis: {competicoes_disponiveis}")
    
    print("✅ Testes básicos concluídos!")

def mostrar_credenciais():
    """Mostra as credenciais de login dos atletas de teste"""
    print("\n🔑 Credenciais de Login:")
    print("=" * 50)
    
    atletas = AtletaUser.objects.all()
    for atleta in atletas:
        inscricao = atleta.get_inscricoes().first()
        if inscricao:
            print(f"👤 {atleta.nome_completo}")
            print(f"   📧 Email: {atleta.email}")
            print(f"   🔒 Senha: {inscricao.senha_atleta}")
            print(f"   📊 Inscrições: {atleta.get_inscricoes().count()}")
            print()

def main():
    """Função principal"""
    print("🎯 Portal do Atleta - Script de Teste Completo")
    print("=" * 60)
    
    try:
        # Criar dados de teste
        atletas = criar_dados_completos()
        
        # Testar funcionalidades
        testar_funcionalidades()
        
        # Mostrar credenciais
        mostrar_credenciais()
        
        print("\n🎉 Portal do Atleta configurado e pronto para uso!")
        print("\n🌐 Acesse: http://localhost:8000/portal-atleta/")
        print("   Use as credenciais mostradas acima para fazer login.")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
