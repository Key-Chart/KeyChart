from django.shortcuts import render

def portal_atleta(request):
    return render(request, 'portal_atleta/portal_atleta.html')