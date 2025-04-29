from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('dashboard/', views.dasboard, name='dashboard'),
    path('sidebar/', views.sidebar),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
