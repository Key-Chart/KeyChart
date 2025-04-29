from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dasboard, name='dashboard'),
    path('sidebar/', views.sidebar),
]
