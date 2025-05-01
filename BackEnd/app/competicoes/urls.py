from django.urls import path
from . import views

app_name = 'competicoes'

urlpatterns = [
    path('', views.competicoes, name='home'),
    path('categoria', views.categoria, name='categoria'),
    path('categoria/atletas_categoria', views.atletas_categoria, name='atletas_categoria'),
    path('categoria/atletas_categoria/chaveamento_kata', views.chaveamento_kata, name='chaveamento_kata'),
]
