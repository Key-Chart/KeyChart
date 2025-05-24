from django.urls import path
from . import views
#from .views import criar_competicao, editar_competicao, excluir_competicao

app_name = 'autenticacao'

urlpatterns = [
    path('', views.login, name='login'),
    #path('criar/', views.criar_competicao, name='criar_competicao'),
]