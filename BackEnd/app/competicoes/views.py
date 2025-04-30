from django.shortcuts import render

def competicoes(request):
    return render(request, 'competicoes/competicoes.html')

def categoria(request):
    return render(request, 'competicoes/categoria.html')