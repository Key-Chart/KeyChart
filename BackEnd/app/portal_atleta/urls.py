from django.urls import path
from . import views

app_name = 'portal_atleta'

from django.urls import path
from . import views

app_name = 'portal_atleta'

urlpatterns = [
    # Autenticação
    path('', views.login_atleta, name='login'),
    path('login/', views.login_atleta, name='login'),
    path('logout/', views.logout_atleta, name='logout'),
    
    # Dashboard principal
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Inscrições
    path('inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),
    path('inscricoes/<uuid:uuid_inscricao>/', views.detalhes_inscricao, name='detalhes_inscricao'),
    
    # Competições
    path('competicoes/', views.competicoes, name='competicoes'),
    path('competicao/<int:competicao_id>/', views.competicao_detalhes, name='competicao_detalhes'),
    path('competicao/<int:competicao_id>/favoritar/', views.favoritar_competicao, name='favoritar_competicao'),
    path('minhas-competicoes/', views.minhas_competicoes, name='minhas_competicoes'),
    
    # Notificações
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('notificacoes/marcar-lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    
    # Configurações e perfil
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/atualizar/', views.atualizar_perfil, name='atualizar_perfil'),
    path('perfil/endereco/', views.atualizar_endereco, name='atualizar_endereco'),
    path('perfil/excluir/', views.excluir_conta, name='excluir_conta'),
]