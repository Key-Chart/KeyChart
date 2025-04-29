from django.urls import path
from . import views

app_name = 'competicoes'

urlpatterns = [
    path('competicoes/', views.competicoes, name='home'),
]
