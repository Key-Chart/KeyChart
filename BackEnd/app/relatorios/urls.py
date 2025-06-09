from django.urls import path
from . import views

app_name = 'relatorio'

urlpatterns = [
    path('', views.relatorio, name='home'),
]