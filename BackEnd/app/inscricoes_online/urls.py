from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'inscricoes_online'

urlpatterns = [
    # Página principal - lista competições abertas
    path('', views.competicoes_abertas, name='home'),
    
    # Inscrição em competição específica
    path('competicao/<int:competicao_id>/', views.inscricao_competicao, name='inscricao'),
    
    # Processar formulário de inscrição
    path('competicao/<int:competicao_id>/processar/', views.processar_inscricao, name='processar'),
    
    # APIs AJAX
    path('api/categorias/<int:competicao_id>/', views.listar_categorias_competicao, name='api_categorias'),
    
    # Status da inscrição
    path('<uuid:uuid>/status/', views.status_inscricao, name='status'),
    
    # Confirmar pagamento (simulação para testes)
    path('<uuid:uuid>/confirmar-pagamento/', views.confirmar_pagamento, name='confirmar_pagamento'),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
