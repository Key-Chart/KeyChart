from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.atletas import views as atletas_views
from django.http import HttpResponseNotFound
urlpatterns = [
    path('admin/', admin.site.urls),
    path('keychart/', include('app.dashboard.urls')),
    path('keychart/competicoes/', include('app.competicoes.urls')),
    path('keychart/equipes_atletas/', include('app.atletas.urls')),
    path('keychart/login/', include('app.autenticacao.urls')),
    path('keychart/portal_atleta/', include('app.portal_atleta.urls')),
    path('keychart/login/', include('app.autenticacao.urls')),
    path('keychart/configuracoes/', include('app.configuracoes.urls')),
    path('keychart/', include('app.partidas_chaveamento.urls')),
    path('keychart/relatorio/', include('app.relatorios.urls')),
    path('keychart/estatisticas/', include('app.estatisticas.urls')),

    path('.well-known/appspecific/com.chrome.devtools.json', lambda r: HttpResponseNotFound()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)