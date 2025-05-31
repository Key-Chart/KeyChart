from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseNotFound

app_name = 'equipes_atletas'

urlpatterns = [
    path('', views.atletas, name='home'),
    path('perfil_atleta/', views.perfil_atleta, name='perfil_atleta'),
    path('inscricoes/', views.inscricoes_view, name='inscricoes'),
    path('carregar_categorias/<int:competicao_id>/', views.carregar_categorias, name='carregar_categorias'),
    path('finalizar_inscricao/', views.finalizar_inscricao, name='finalizar_inscricao'),
    path('enviar_email_inscricao/', views.enviar_email_inscricao, name='enviar_email_inscricao'),
    path('atletas/', views.atletas, name='atletas'),
    #path('atletas/desativar/', views.desativar_atleta, name='desativar_atleta'),
    #path('atletas/ativar/', views.ativar_atleta, name='ativar_atleta'),
    #path('atletas/editar/<int:atleta_id>/', views.editar_atleta, name='editar_atleta'),
    path('atletas/perfil/<int:atleta_id>/', views.perfil_atleta, name='perfil_atleta'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
