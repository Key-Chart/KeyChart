from django.shortcuts import render

# View para a página de dashboard
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# View para a sidebar
def sidebar(request):
    return render(request, 'dashboard/sidebar.html')
