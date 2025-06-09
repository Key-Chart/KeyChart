from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    # Competição
    path('', views.configuracoes, name='home'),
]