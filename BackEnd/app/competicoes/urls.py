from django.urls import path
from . import views

app_name = 'competicoes'

urlpatterns = [
    path('', views.competicoes, name='home'),
    path('categoria', views.categoria),
]
