from django.shortcuts import render
from app.autenticacao.decorators import login_required_custom

# View para a página de dashboard
#@login_required_custom
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# View para a sidebar
def sidebar(request):
    return render(request, 'dashboard/sidebar.html')
