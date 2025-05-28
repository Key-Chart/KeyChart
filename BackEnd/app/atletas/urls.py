from django.urls import path
from . import views
from django.http import HttpResponseNotFound

app_name = 'equipes_atletas'

urlpatterns = [
    path('', views.atletas, name='home'),
    path('perfil_atleta/', views.perfil_atleta, name='perfil_atleta'),
    path('inscricoes/', views.inscricoes_view, name='inscricoes'),
    path('keychart/inscricoes/', views.inscricoes_view, name='inscricoes'),
    path('keychart/carregar_categorias/<int:competicao_id>/', views.carregar_categorias, name='carregar_categorias'),
    path('keychart/finalizar_inscricao/', views.finalizar_inscricao, name='finalizar_inscricao'),
    path('keychart/enviar_email_inscricao/', views.enviar_email_inscricao, name='enviar_email_inscricao'),
]