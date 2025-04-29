from django.shortcuts import render

def competicoes(request):
    return render(request, 'competicoes.html')