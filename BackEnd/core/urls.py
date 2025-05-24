from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('keychart/dashboard/', include('app.dashboard.urls')),
    path('keychart/competicoes/', include('app.competicoes.urls')),
    path('keychart/login/', include('app.autenticacao.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)