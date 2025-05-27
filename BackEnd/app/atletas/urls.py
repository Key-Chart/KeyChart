from django.urls import path
from . import views

app_name = 'equipes_atletas'

urlpatterns = [
    path('', views.atletas, name='home'),
    path('perfil_atleta/', views.perfil_atleta, name='perfil_atleta'),
]