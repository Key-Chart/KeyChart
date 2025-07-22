#!/usr/bin/env python
"""
Script para testar o Portal do Atleta integrado com o sistema de inscrições
Cria dados de teste e demonstra todas as funcionalidades
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

def criar_dados_teste():
    """Cria dados de teste para o portal do atleta"""
    print("🚀 Criando dados de teste para o Portal do Atleta...")
    
    # 1. Criar competição de teste
    competicao, created = Competicao.objects.get_or_create(
        nome="Campeonato Paulista de Karatê 2025",
        defaults={
            'descricao': 'Campeonato estadual de karatê com várias categorias',
            'data_inicio': timezone.now().date() + timedelta(days=30),
            'data_fim': timezone.now().date() + timedelta(days=32),
            'local': 'Centro de Convenções - São Paulo, SP',
            'valor_inscricao': 150.00,
            'data_limite_inscricao': timezone.now().date() + timedelta(days=15),
            'status': 'ativa',
            'organizador': 'Federação Paulista de Karatê',
            'contato_organizador': 'contato@fpk.org.br',
            'limite_inscricoes': 500
        }
    )
    print(f"✅ Competição criada: {competicao.nome}")
    
    # 2. Criar categoria de teste
    categoria, created = Categoria.objects.get_or_create(
        nome="Kata Individual Adulto Masculino",
        competicao=competicao,
        defaults={
            'descricao': 'Categoria para kata individual masculino adulto',
            'idade_minima': 18,
            'idade_maxima': 50,
            'peso_minimo': 0,
            'peso_maximo': 999,
            'graduacao_minima': 'Faixa Branca',
            'graduacao_maxima': 'Faixa Preta',
            'sexo': 'M'
        }
    )
    print(f"✅ Categoria criada: {categoria.nome}")
    
    # 3. Criar inscrições de teste
    atletas_teste = [
        {
            'nome': 'João Silva Santos',
            'email': 'joao.silva@email.com',
            'cpf': '123.456.789-01',
            'telefone': '(11) 99999-1111',
            'data_nascimento': '1990-05-15'
        },
        {
            'nome': 'Maria Oliveira Costa',
            'email': 'maria.oliveira@email.com',
            'cpf': '987.654.321-09',
            'telefone': '(11) 99999-2222',
            'data_nascimento': '1992-08-20'
        },
        {
            'nome': 'Carlos Eduardo Lima',
            'email': 'carlos.lima@email.com',
            'cpf': '456.789.123-45',
            'telefone': '(11) 99999-3333',
            'data_nascimento': '1988-12-10'
        }
    ]
    
    inscricoes_criadas = []
    
    for i, atleta_data in enumerate(atletas_teste):
        # Criar inscrição online
        inscricao, created = InscricaoOnline.objects.get_or_create(
            email=atleta_data['email'],
            competicao=competicao,
            defaults={
                'nome_completo': atleta_data['nome'],
                'cpf': atleta_data['cpf'],
                'telefone': atleta_data['telefone'],
                'data_nascimento': atleta_data['data_nascimento'],
                'categoria': categoria,
                'valor_inscricao': competicao.valor_inscricao,
                'status': 'confirmada' if i < 2 else 'paga',
                'data_limite_pagamento': timezone.now().date() + timedelta(days=7),
                'observacoes': f'Atleta teste {i+1} criado automaticamente'
            }
        )
        
        if created:
            inscricoes_criadas.append(inscricao)
            print(f"✅ Inscrição criada: {inscricao.nome_completo}")
            
            # Criar usuário do portal para cada inscrição
            criar_usuario_portal(inscricao)
    
    return inscricoes_criadas

def criar_usuario_portal(inscricao):
    """Cria usuário do portal baseado na inscrição"""
    try:
        # Verificar se já existe usuário para este email
        atleta_user, created = AtletaUser.objects.get_or_create(
            email=inscricao.email,
            defaults={
                'nome_completo': inscricao.nome_completo,
                'telefone': inscricao.telefone,
                'inscricao_origem': inscricao,
                'password': make_password('senha123'),  # Senha padrão para testes
                'is_active': True,
                'email_verificado': True,
                'primeiro_acesso': False,
                'ultimo_acesso': timezone.now()
            }
        )
        
        if created:
            print(f"✅ Usuário portal criado: {atleta_user.email}")
            
            # Criar preferências padrão
            criar_preferencias_padrao(atleta_user)
            
            # Criar notificações de teste
            criar_notificacoes_teste(atleta_user)
            
        return atleta_user
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário portal: {e}")
        return None

def criar_preferencias_padrao(atleta_user):
    """Cria preferências padrão para o atleta"""
    try:
        preferencia, created = PreferenciaAtleta.objects.get_or_create(
            atleta=atleta_user,
            defaults={
                'receber_email_inscricao': True,
                'receber_email_pagamento': True,
                'receber_email_competicao': True,
                'receber_email_resultado': True,
                'perfil_publico': False,
                'mostrar_resultados': True,
                'mostrar_estatisticas': True,
                'tema_escuro': False,
                'idioma': 'pt-br'
            }
        )
        
        if created:
            print(f"✅ Preferências criadas para: {atleta_user.email}")
            
    except Exception as e:
        print(f"❌ Erro ao criar preferências: {e}")

def criar_notificacoes_teste(atleta_user):
    """Cria notificações de teste para o atleta"""
    notificacoes = [
        {
            'tipo': 'inscricao',
            'titulo': 'Inscrição Confirmada',
            'mensagem': 'Sua inscrição no Campeonato Paulista de Karatê 2025 foi confirmada com sucesso!',
            'prioridade': 'alta',
            'lida': False
        },
        {
            'tipo': 'pagamento',
            'titulo': 'Pagamento Pendente',
            'mensagem': 'Lembrete: O pagamento da sua inscrição vence em 7 dias. Não perca o prazo!',
            'prioridade': 'normal',
            'lida': False
        },
        {
            'tipo': 'competicao',
            'titulo': 'Cronograma Disponível',
            'mensagem': 'O cronograma detalhado da competição já está disponível. Confira seus horários!',
            'prioridade': 'normal',
            'lida': True
        },
        {
            'tipo': 'sistema',
            'titulo': 'Bem-vindo ao Portal',
            'mensagem': 'Bem-vindo ao Portal do Atleta! Aqui você pode acompanhar todas as suas inscrições e resultados.',
            'prioridade': 'baixa',
            'lida': True
        }
    ]
    
    for notif_data in notificacoes:
        try:
            NotificacaoAtleta.objects.create(
                atleta=atleta_user,
                tipo=notif_data['tipo'],
                titulo=notif_data['titulo'],
                mensagem=notif_data['mensagem'],
                prioridade=notif_data['prioridade'],
                lida=notif_data['lida'],
                data_leitura=timezone.now() if notif_data['lida'] else None
            )
            print(f"✅ Notificação criada: {notif_data['titulo']}")
            
        except Exception as e:
            print(f"❌ Erro ao criar notificação: {e}")

def testar_funcionalidades():
    """Testa as principais funcionalidades do portal"""
    print("\n🧪 Testando funcionalidades do Portal do Atleta...")
    
    # Testar criação de usuário
    print("\n1. Testando criação de usuário:")
    atletas = AtletaUser.objects.all()[:3]
    for atleta in atletas:
        print(f"   - {atleta.email}: {atleta.get_nome_completo()}")
    
    # Testar notificações
    print("\n2. Testando notificações:")
    for atleta in atletas:
        total = atleta.notificacoes.count()
        nao_lidas = atleta.notificacoes.filter(lida=False).count()
        print(f"   - {atleta.email}: {total} total, {nao_lidas} não lidas")
    
    # Testar preferências
    print("\n3. Testando preferências:")
    for atleta in atletas:
        try:
            pref = atleta.preferencias
            print(f"   - {atleta.email}: Email inscrição={pref.receber_email_inscricao}, Tema escuro={pref.tema_escuro}")
        except PreferenciaAtleta.DoesNotExist:
            print(f"   - {atleta.email}: Sem preferências configuradas")
    
    # Testar inscrições relacionadas
    print("\n4. Testando inscrições relacionadas:")
    for atleta in atletas:
        inscricoes = InscricaoOnline.objects.filter(email=atleta.email)
        print(f"   - {atleta.email}: {inscricoes.count()} inscrições")
        for inscricao in inscricoes:
            print(f"     * {inscricao.competicao.nome} - Status: {inscricao.status}")

def exibir_credenciais():
    """Exibe as credenciais de acesso para teste"""
    print("\n🔑 Credenciais de Acesso para Teste:")
    print("=" * 50)
    
    atletas = AtletaUser.objects.all()[:3]
    for i, atleta in enumerate(atletas, 1):
        print(f"\nAtleta {i}:")
        print(f"  Email: {atleta.email}")
        print(f"  Senha: senha123")
        print(f"  Nome: {atleta.get_nome_completo()}")
        print(f"  Status: {'Ativo' if atleta.is_active else 'Inativo'}")
    
    print(f"\n📍 URL de Acesso: http://localhost:8000/keychart/portal_atleta/")
    print("=" * 50)

def limpar_dados_teste():
    """Remove todos os dados de teste"""
    resposta = input("\n⚠️  Deseja limpar todos os dados de teste? (s/N): ")
    if resposta.lower() == 's':
        print("🧹 Limpando dados de teste...")
        
        # Remover usuários de teste
        AtletaUser.objects.filter(email__contains='@email.com').delete()
        print("✅ Usuários de teste removidos")
        
        # Remover inscrições de teste
        InscricaoOnline.objects.filter(observacoes__contains='Atleta teste').delete()
        print("✅ Inscrições de teste removidas")
        
        print("✅ Limpeza concluída!")

def main():
    """Função principal"""
    print("🏆 Portal do Atleta - Sistema de Testes")
    print("=" * 50)
    
    try:
        # Criar dados de teste
        inscricoes = criar_dados_teste()
        
        # Testar funcionalidades
        testar_funcionalidades()
        
        # Exibir credenciais
        exibir_credenciais()
        
        print("\n✅ Sistema de teste configurado com sucesso!")
        print("\n💡 Dicas:")
        print("   - Acesse o portal com as credenciais acima")
        print("   - Teste todas as funcionalidades do dashboard")
        print("   - Verifique as notificações e configurações")
        print("   - Experimente as diferentes páginas do portal")
        
        # Opção de limpeza
        limpar_dados_teste()
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
