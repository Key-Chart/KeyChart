from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.atletas import views as atletas_views
from django.http import HttpResponseNotFound
urlpatterns = [
    path('admin/', admin.site.urls),
    path('keychart/dashboard/', include('app.dashboard.urls')),
    path('keychart/competicoes/', include('app.competicoes.urls')),
    path('keychart/equipes_atletas/', include('app.atletas.urls')),
    path('keychart/inscricoes/', atletas_views.inscricoes_view, name='inscricoes'),
    path('keychart/login/', include('app.autenticacao.urls')),
    path('.well-known/appspecific/com.chrome.devtools.json', lambda r: HttpResponseNotFound()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)