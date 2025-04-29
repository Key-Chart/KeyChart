from django.shortcuts import render, HttpResponse

def dasboard(request):
    return render(request, 'dashboard.html')

def sidebar(request):
    return render(request, 'sidebar.html')