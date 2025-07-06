from django.urls import path
from . import views

app_name = 'portal_atleta'

urlpatterns = [
    # Portal Atletas
    path('', views.portal_atleta, name='portal_atleta'),
    path('<int:atleta_id>/', views.portal_atleta, name='portal_atleta_especifico'),
    path('competicao/<int:competicao_id>/', views.detalhes_competicao, name='detalhes_competicao'),
    path('resultados/', views.meus_resultados, name='meus_resultados'),
    path('resultados/<int:atleta_id>/', views.meus_resultados, name='meus_resultados_especifico'),
]