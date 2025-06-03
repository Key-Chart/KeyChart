from django.urls import path
from . import views

app_name = 'competicoes'

urlpatterns = [
    # Competição
    path('', views.competicoes, name='home'),
    path('criar/', views.criar_competicao, name='criar_competicao'),
    path('editar/<int:competicao_id>/', views.editar_competicao, name='editar_competicao'),
    path('excluir/<int:competicao_id>/', views.excluir_competicao, name='excluir_competicao'),

    # Categorias
    path('categorias/', views.categoria_home, name='categoria_home'),
    path('competicao/<int:competicao_id>/categorias/', views.categoria, name='categoria'),
    path('categoria/<int:categoria_id>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    path('categoria/<int:categoria_id>/atletas/chaveamento_kata/', views.chaveamento_kata, name='chaveamento_kata'),
    path('categoria/atletas/chaveamento_kumite', views.chaveamento_kumite, name='chaveamento_kumite'),
    path('categoria/atletas/chaveamento_kumite_teste', views.chaveamento_kumite_teste, name='chaveamento_kumite_teste'),
    path('competicao/<int:competicao_id>/categoria/cadastrar/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('categoria/<int:categoria_id>/atletas/', views.atletas_categoria, name='atletas_categoria'),

    # Academias
    path('academia/cadastrar/', views.cadastrar_academia, name='cadastrar_academia'),
    path('academia/<int:academia_id>/editar/', views.editar_academia, name='editar_academia'),
    path('academia/<int:academia_id>/excluir/', views.excluir_academia, name='excluir_academia'),

    # Atletas Categoria
    path('atleta/<int:pk>/editar/', views.editar_atleta, name='atleta_editar'),
]