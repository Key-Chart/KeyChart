from django.shortcuts import render

def atletas(request):
    return render(request, 'atletas/equipes_atletas.html')

def perfil_atleta(request):
    return render(request, 'atletas/perfil_atleta.html')