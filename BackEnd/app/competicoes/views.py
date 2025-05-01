from django.shortcuts import render

def competicoes(request):
    return render(request, 'competicoes/competicoes.html')

def categoria(request):
    return render(request, 'competicoes/categoria.html')

def atletas_categoria(request):
    return render(request, 'competicoes/atletas_categoria.html')

def chaveamento_kata(request):
    return render(request, 'competicoes/chaveamento_kata.html')