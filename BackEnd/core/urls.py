from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.atletas import views as atletas_views
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/keychart/')),  # Redireciona a raiz para /keychart/
    path('admin/', admin.site.urls),
    path('keychart/', include('app.dashboard.urls')),
    path('keychart/competicoes/', include('app.competicoes.urls')),
    path('keychart/equipes_atletas/', include('app.atletas.urls')),
    path('keychart/login/', include('app.autenticacao.urls')),
    path('portal-atleta/', include('app.portal_atleta.urls')),  # Portal do atleta com URL simplificada
    path('keychart/login/', include('app.autenticacao.urls')),
    path('keychart/configuracoes/', include('app.configuracoes.urls')),
    path('keychart/', include('app.partidas_chaveamento.urls')),
    path('keychart/relatorio/', include('app.relatorios.urls')),
    path('keychart/estatisticas/', include('app.estatisticas.urls')),
    path('inscricoes/', include('app.inscricoes_online.urls')),

    path('.well-known/appspecific/com.chrome.devtools.json', lambda r: HttpResponseNotFound()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)