from django.urls import path
from . import views

app_name = 'partidas_chaveamento'

urlpatterns = [
    path('partidas/', views.partidas, name='home'),
    path('chaveamento/', views.chaveamento, name='chaveamento'),
]