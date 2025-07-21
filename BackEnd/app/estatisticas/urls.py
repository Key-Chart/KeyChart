from django.urls import path
from . import views

app_name = 'estatisticas'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_view, name='dashboard'),
    
    # Páginas específicas
    path('competicoes/', views.competicoes_stats_view, name='competicoes'),
    path('atletas/', views.atletas_stats_view, name='atletas'),
    path('academias/', views.academias_stats_view, name='academias'),
    path('comparativas/', views.comparativas_view, name='comparativas'),
    
    # APIs para dados em tempo real
    path('api/metricas/', views.MetricasAPIView.as_view(), name='api_metricas'),
    path('api/graficos/', views.GraficosAPIView.as_view(), name='api_graficos'),
    path('api/kpis/', views.KPIsAPIView.as_view(), name='api_kpis'),
    path('api/alertas/', views.alertas_api_view, name='api_alertas'),
    path('api/export/', views.export_api_view, name='api_export'),
]
