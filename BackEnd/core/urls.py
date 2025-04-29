from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('keychart/', include('dashboard.urls')),
    path('keychart/', include('competicoes.urls')),
]
