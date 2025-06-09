from django.urls import path
from . import views

app_name = 'portal_atleta'

urlpatterns = [
    # Portal Atletas
    path('', views.portal_atleta, name='portal_atleta'),
]