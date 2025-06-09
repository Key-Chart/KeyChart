from django.shortcuts import render

# Rota para renderizar a pagina de Partidas
def partidas(request):
    return render(request, 'partidas_chaveamento/partidas.html')

def chaveamento(request):
    return render(request, 'partidas_chaveamento/chaveamento.html')