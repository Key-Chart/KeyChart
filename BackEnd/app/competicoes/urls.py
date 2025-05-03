from django.urls import path
from . import views
from .views import criar_competicao, editar_competicao, excluir_competicao

app_name = 'competicoes'

urlpatterns = [
    path('', views.competicoes, name='home'),
    path('criar/', views.criar_competicao, name='criar_competicao'),
    path('editar/<int:competicao_id>/', editar_competicao, name='editar_competicao'),
    path('excluir/<int:competicao_id>/', excluir_competicao, name='excluir_competicao'),
    path('categoria', views.categoria, name='categoria'),
    path('categoria/atletas_categoria', views.atletas_categoria, name='atletas_categoria'),
    path('categoria/atletas_categoria/chaveamento_kata', views.chaveamento_kata, name='chaveamento_kata'),
]
