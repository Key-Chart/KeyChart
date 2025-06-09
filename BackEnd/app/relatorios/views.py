from django.shortcuts import render

def relatorio(request):
    return render(request, 'relatorios/relatorio.html')